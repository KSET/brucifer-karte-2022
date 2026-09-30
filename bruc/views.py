import hmac
import json
from datetime import datetime, time, timedelta
from uuid import uuid4

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.utils.timezone import make_aware
from django.views.decorators.cache import never_cache
from django_filters.rest_framework import DjangoFilterBackend
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Translations, Visibility, Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact, Mailer, GameLeaderboard, BrucosiFormResponse
from .roles import Role, GUEST_ROLES
from .serializer import BrucosiFormResponseSerializer, TranslationsSerializer, VisibilitySerializer, CjenikSerializer, GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer, DynamicSearchFilter, MailerSerializer, GameLeaderboardSerializer, PublicLineupSerializer, PublicSponsorsSerializer, PublicGuestSerializer
from .services import derive_fer_email, send_guest_ticket_email

class SponsorGuestThrottle(AnonRateThrottle):
    rate = '30/hour'

class MailerThrottle(AnonRateThrottle):
    rate = '200/hour'

class FormThrottle(AnonRateThrottle):
    rate = '100/hour'


MAX_BULK_RECORDS = 5000
FAILED_MAIL_STATUSES = ('failed', 'bounced')


def _caller_role(request):
    """Role-key of the JWT caller (Users.privilege), or None if unauthenticated."""
    if not request.user or not request.user.is_authenticated:
        return None
    try:
        user = Users.objects.get(email=request.user.username)
        return user.privilege
    except Users.DoesNotExist:
        return None


def HasRole(*roles):
    """Allow callers whose role is one of `roles` (no implicit hierarchy)."""
    allowed = set(roles)

    class _HasRole(BasePermission):
        def has_permission(self, request, view):
            return _caller_role(request) in allowed

    return _HasRole


def ReadOnlyOrRole(*write_roles, read_roles=None):
    """Reads: open when `read_roles` is None, else restricted to it. Writes: `write_roles`."""
    write_allowed = set(write_roles)
    read_allowed = None if read_roles is None else set(read_roles)

    class _ReadOnlyOrRole(BasePermission):
        def has_permission(self, request, view):
            if request.method in SAFE_METHODS:
                if read_allowed is None:
                    return True
                return _caller_role(request) in read_allowed
            return _caller_role(request) in write_allowed

    return _ReadOnlyOrRole

class MailerViewSet(viewsets.ModelViewSet):
    queryset = Mailer.objects.all()
    serializer_class = MailerSerializer
    permission_classes = [HasRole(Role.ADMIN)]

    @action(detail=False, methods=['post'], throttle_classes=[MailerThrottle])
    def send_mail(self, request):
        emails = request.data.get('emails', [])  # Expecting a list of email details

        messages = []
        guest_results = []
        for email in emails:
            subject = email.get('subject', '')
            msg = email.get('message', '')
            to = email.get('to_mail', '')
            template_name = email.get('template', '')
            html_message = ''

            if template_name == "user_email":
                html_message = render_to_string('emails/user_email.html', {
                    'name': email.get('name', ''), 'privilege_name': email.get('privilege_name', ''), })
            elif template_name == "guest_email":
                conf_code = email.get('confCode') or ''
                guest = Guests.objects.filter(confCode=conf_code).first() if conf_code else None
                guest_results.append(send_guest_ticket_email(guest)[0] if guest else False)
                continue
            elif template_name == "sponsors_email":
                sponsor = Sponsors.objects.filter(slug=(email.get('slug') or '')).first()
                if not sponsor:
                    continue
                link = f"https://brucosijada.kset.org/sponzori/{sponsor.slug}/{sponsor.access_token}"
                html_message = render_to_string('emails/sponsors_email.html', {
                    'name': email.get('name', ''), 'link': link})

            if subject and msg and to and html_message:
                text_content = strip_tags(html_message)
                msg = EmailMultiAlternatives(subject, text_content, f"43. Brucifer <{settings.DEFAULT_FROM_EMAIL}>", [to])
                msg.attach_alternative(html_message, "text/html")
                messages.append(msg)

        if messages:
            try:
                with get_connection() as connection:
                    connection.send_messages(messages)
            except Exception:
                return HttpResponse('Failed to send emails.', status=500)
        if not messages and not guest_results:
            return HttpResponse('Make sure all fields are entered and valid for each email.')
        if not all(guest_results):
            return HttpResponse('Failed to send emails.', status=500)
        return HttpResponse('Emails sent successfully.')


class GuestsViewSet(viewsets.ModelViewSet):
    queryset = Guests.objects.all()
    serializer_class = GuestsSerializer
    filter_backends = [DynamicSearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'surname', 'tag', 'confCode', 'jmbag', 'email']
    filterset_fields = ['bought', 'entered']
    permission_classes = [HasRole(*GUEST_ROLES)]

    @action(detail=False, methods=['post'], url_path='bulk-import')
    def bulk_import(self, request):
        try:
            guests_data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(guests_data, list):
            return Response({'error': 'Expected a JSON list'}, status=status.HTTP_400_BAD_REQUEST)
        if len(guests_data) > MAX_BULK_RECORDS:
            return Response({'error': f'Too many records (max {MAX_BULK_RECORDS})'},
                            status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        guests_serializer = GuestsSerializer(data=guests_data, many=True)  # 'many=True' is important for bulk operations
        
        if guests_serializer.is_valid():
            # Using atomic transactions to ensure all-or-nothing
            with transaction.atomic():
                Guests.objects.bulk_create([Guests(**data) for data in guests_serializer.validated_data])
                return Response({'message': 'Bulk guests import successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(guests_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='search-brucosi')
    def search_brucosi(self, request):
        jmbag = (request.query_params.get('jmbag') or '').strip()
        if not jmbag:
            return Response({"error": "Missing jmbag parameter"}, status=status.HTTP_400_BAD_REQUEST)

        guests = list(Guests.objects.filter(jmbag__startswith=jmbag, tag="Brucoši")[:2])
        if len(guests) != 1:
            count = Guests.objects.filter(jmbag__startswith=jmbag, tag="Brucoši").count() if guests else 0
            return Response({"count": count, "guests": [], "submissions": []})

        submissions = BrucosiFormResponse.objects.filter(jmbag=guests[0].jmbag)

        seen = set()
        unique_submissions = []
        for s in submissions:
            key = (s.name.strip().lower(), s.surname.strip().lower())
            if key not in seen:
                seen.add(key)
                unique_submissions.append(s)

        guest_data = GuestsSerializer(guests, many=True).data
        submission_data = BrucosiFormResponseSerializer(unique_submissions, many=True).data

        return Response({
            "count": 1,
            "guests": guest_data,
            "submissions": submission_data
        })
    
    @action(detail=False, methods=["get"], url_path="today-stats")
    def today_stats(self, request):
        today = timezone.localdate()
        today_start = make_aware(datetime.combine(today, time.min))
        noon_time = make_aware(datetime.combine(today, time(12, 0)))
        tomorrow_start = make_aware(datetime.combine(today + timedelta(days=1), time.min))

        brucosi = Guests.objects.filter(tag="Brucoši")
        guests = brucosi.filter(boughtTicketTime__gte=today_start, boughtTicketTime__lt=tomorrow_start)

        total_entries = guests.count()
        tickets_before_12 = guests.filter(boughtTicketTime__lt=noon_time).count()
        tickets_after_12 = guests.filter(boughtTicketTime__gte=noon_time).count()

        return Response({
            "date": today.isoformat(),
            "totalEntries": total_entries,
            "ticketsBefore12": tickets_before_12,
            "ticketsAfter12": tickets_after_12,
            "failedMails": brucosi.filter(bought=True, mailStatus__in=FAILED_MAIL_STATUSES).count(),
        })

    @staticmethod
    def _sale_names(request, guest):
        is_admin = _caller_role(request) == Role.ADMIN
        submissions = BrucosiFormResponse.objects.filter(jmbag=guest.jmbag)
        result = []
        for field in ('name', 'surname'):
            stored = getattr(guest, field).strip()
            submitted = sorted({getattr(s, field).strip() for s in submissions} - {''})
            value = stored or (submitted[0] if len(submitted) == 1 else '')
            body = str(request.data.get(field) or '').strip()
            if body and (is_admin or stored or submitted):
                value = body
            result.append(value)
        return result

    @action(detail=True, methods=['post'], url_path='sell',
            permission_classes=[HasRole(Role.TICKETS, Role.ENTRY_TICKETS, Role.ADMIN)])
    def sell(self, request, pk=None):
        guest = self.get_object()
        if guest.tag != "Brucoši":
            return Response({"detail": "Gost nije brucoš."}, status=status.HTTP_400_BAD_REQUEST)

        name, surname = self._sale_names(request, guest)
        if not name or not surname:
            return Response({"detail": "Nedostaje ime/prezime – brucoš nije ispunio formu."},
                            status=status.HTTP_400_BAD_REQUEST)
        email = derive_fer_email(name, surname, guest.jmbag)
        if not email:
            return Response({"detail": "Nije moguće odrediti email adresu."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            claimed = Guests.objects.filter(pk=guest.pk, bought=False).update(
                bought=True, confCode=str(uuid4()), boughtTicketTime=timezone.now(),
                name=name, surname=surname, email=email,
                mailStatus='none', mailError='', mailSentAt=None, mailMessageId='')
            if not claimed:
                return Response({"detail": "Karta je već prodana."}, status=status.HTTP_409_CONFLICT)
            BrucosiFormResponse.objects.filter(jmbag=guest.jmbag).update(status='redeemed')

        guest.refresh_from_db()
        mail_sent, mail_error = send_guest_ticket_email(guest)
        return Response({
            "guest": GuestsSerializer(guest).data,
            "email": email,
            "mail_sent": mail_sent,
            "mail_error": mail_error,
        })

    @action(detail=True, methods=['post'], url_path='unsell', permission_classes=[HasRole(Role.ADMIN)])
    def unsell(self, request, pk=None):
        guest = self.get_object()
        with transaction.atomic():
            cleared = Guests.objects.filter(pk=guest.pk, entered=False).update(
                bought=False, confCode='', boughtTicketTime=None,
                mailStatus='none', mailError='', mailSentAt=None, mailMessageId='')
            if not cleared:
                return Response({"detail": "Gost je već ušao, prodaja se ne može poništiti."},
                                status=status.HTTP_409_CONFLICT)
            BrucosiFormResponse.objects.filter(jmbag=guest.jmbag).update(status='invalid')
        guest.refresh_from_db()
        return Response({"guest": GuestsSerializer(guest).data})

    @action(detail=True, methods=['post'], url_path='resend-mail', permission_classes=[HasRole(Role.ADMIN)])
    def resend_mail(self, request, pk=None):
        guest = self.get_object()
        if not guest.bought or not guest.confCode:
            return Response({"detail": "Karta nije prodana."}, status=status.HTTP_400_BAD_REQUEST)

        name = str(request.data.get('name') or '').strip()
        surname = str(request.data.get('surname') or '').strip()
        if name or surname:
            guest.name = name or guest.name
            guest.surname = surname or guest.surname
            guest.save(update_fields=['name', 'surname'])

        mail_sent, mail_error = send_guest_ticket_email(guest)
        return Response({
            "guest": GuestsSerializer(guest).data,
            "email": guest.email,
            "mail_sent": mail_sent,
            "mail_error": mail_error,
        })

    @action(detail=False, methods=['get'], url_path='failed-mails', permission_classes=[HasRole(Role.ADMIN)])
    def failed_mails(self, request):
        guests = Guests.objects.filter(bought=True, mailStatus__in=FAILED_MAIL_STATUSES) \
            .order_by('-boughtTicketTime')
        return Response(GuestsSerializer(guests, many=True).data)

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [ReadOnlyOrRole(Role.ADMIN, read_roles=GUEST_ROLES)]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    permission_classes = [HasRole(Role.ADMIN)]

    @action(detail=False, methods=['post'], url_path='bulk-import')
    def bulk_import(self, request):
        try:
            user_data = json.loads(request.body)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(user_data, list):
            return Response({'error': 'Expected a JSON list'}, status=status.HTTP_400_BAD_REQUEST)
        if len(user_data) > MAX_BULK_RECORDS:
            return Response({'error': f'Too many records (max {MAX_BULK_RECORDS})'},
                            status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        user_serializer = UsersSerializer(data=user_data, many=True)  # 'many=True' is important for bulk operations
        
        if user_serializer.is_valid():
            # Using atomic transactions to ensure all-or-nothing
            with transaction.atomic():
                Users.objects.bulk_create([Users(**data) for data in user_serializer.validated_data])
                return Response({'message': 'Bulk user import successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LineupViewSet(viewsets.ModelViewSet):
    queryset = Lineup.objects.all()
    serializer_class = LineupSerializer
    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['=slug', 'name']
    ordering_fields = ['order']
    permission_classes = [HasRole(Role.ADMIN)]

    @transaction.atomic
    def perform_create(self, serializer):
        last = Lineup.objects.select_for_update().order_by('-order').first()
        next_order = (last.order if last else 0) + 1
        serializer.save(order=next_order, slug=str(uuid4()))

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def reorder(self, request):
        payload = request.data
        if not isinstance(payload, list):
            return Response({"error": "Expected a list of {id, order}."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            pairs = [(int(item["id"]), int(item["order"])) for item in payload]
        except (KeyError, TypeError, ValueError):
            return Response({"error": "Each item must have integer 'id' and 'order'."},
                            status=status.HTTP_400_BAD_REQUEST)

        ids    = [i for i, _ in pairs]
        orders = [o for _, o in pairs]

        if len(set(ids)) != len(ids):
            return Response({"error": "Duplicate ids in payload."}, status=status.HTTP_400_BAD_REQUEST)
        if len(set(orders)) != len(orders):
            return Response({"error": "Duplicate orders in payload."}, status=status.HTTP_400_BAD_REQUEST)
        if any(o < 0 for o in orders):
            return Response({"error": "Order must be non-negative integers."}, status=status.HTTP_400_BAD_REQUEST)

        objs = {obj.id: obj for obj in Lineup.objects.select_for_update().filter(id__in=ids)}
        missing = sorted(set(ids) - set(objs.keys()))
        if missing:
            return Response({"error": f"Lineup(s) not found: {missing}"}, status=status.HTTP_404_NOT_FOUND)

        for _id, _ord in pairs:
            objs[_id].order = _ord
        Lineup.objects.bulk_update(objs.values(), ['order'])

        return Response({"status": "ok"}, status=status.HTTP_200_OK)

class PublicLineupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicLineupSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_queryset(self):
        return Lineup.objects.filter(visible=True).order_by('order')

class SponsorsViewSet(viewsets.ModelViewSet):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer
    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['=slug', 'name', 'email']
    ordering_fields = ['order']
    permission_classes = [HasRole(Role.ADMIN)]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='public')
    def public(self, request):
        """
        GET /api/sponsors/public/?slug=<slug>
        Returns a trimmed, safe payload for the sponsor portal.
        """
        slug = request.query_params.get('slug')
        if not slug:
            return Response({"detail": "slug is required"}, status=400)

        sponsor = Sponsors.objects.filter(slug=slug, visible=True).first()
        if not sponsor:
            return Response({"detail": "Not found"}, status=404)

        serializer = self.get_serializer(sponsor)
        return Response(serializer.data)

    @staticmethod
    def _sponsor_input_open(sponsor):
        if sponsor.guestsEnabled == 2:
            return True
        if sponsor.guestsEnabled != 1:
            return False

        deadline = (
            Visibility.objects.filter(name="SPONSORS_INPUT_TIME")
            .values_list("time", flat=True)
            .first()
        )
        return deadline is None or timezone.now() <= deadline

    @action(
        detail=False,
        methods=['get', 'post', 'delete'],
        permission_classes=[AllowAny],
        throttle_classes=[SponsorGuestThrottle],
        url_path='public/guests'
    )
    def public_guests(self, request):
        """
        GET    /api/sponsors/public/guests/?slug=<slug>
        POST   /api/sponsors/public/guests/
        DELETE /api/sponsors/public/guests/?slug=<slug>&id=<guest_id>
        """

        # ------------------ GET ------------------
        if request.method == 'GET':
            slug = (request.query_params.get("slug") or "").strip()
            access_token = (request.query_params.get("access_token") or "").strip()
            if not slug or not access_token:
                return Response({"detail": "slug and access_token are required"}, status=400)

            sponsor = Sponsors.objects.filter(slug=slug, access_token=access_token).first()
            if not sponsor:
                return Response({"detail": "Sponsor not found"}, status=404)

            tag_prefix = f"{sponsor.slug} "
            qs = Guests.objects.filter(tag__istartswith=tag_prefix).order_by("id")

            return Response(
                PublicGuestSerializer(qs, many=True).data,
                status=200,
            )

        # ------------------ DELETE ------------------
        if request.method == 'DELETE':
            slug = (request.query_params.get("slug") or "").strip()
            guest_id = (request.query_params.get("id") or "").strip()
            access_token = (request.query_params.get("access_token") or "").strip()

            if not slug or not guest_id or not access_token:
                return Response({"detail": "slug, id and access_token are required"}, status=400)

            sponsor = Sponsors.objects.filter(slug=slug, access_token=access_token).first()
            if not sponsor:
                return Response({"detail": "Sponsor not found"}, status=404)

            if not self._sponsor_input_open(sponsor):
                return Response({"detail": "Unos gostiju je zatvoren"}, status=403)

            guest = Guests.objects.filter(id=guest_id, tag__istartswith=f"{sponsor.slug} ").first()
            if not guest:
                return Response({"detail": "Guest not found"}, status=404)

            guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # ------------------ POST ------------------
        slug = (request.data.get("slug") or "").strip()
        name = (request.data.get("name") or "").strip()
        access_token = (request.data.get("access_token") or "").strip()

        if not slug or not name or not access_token:
            return Response({"detail": "slug, name and access_token are required"}, status=400)

        with transaction.atomic():
            sponsor = (
                Sponsors.objects.select_for_update()
                .filter(slug=slug, access_token=access_token)
                .first()
            )
            if not sponsor:
                return Response({"detail": "Sponsor not found"}, status=404)

            if not self._sponsor_input_open(sponsor):
                return Response({"detail": "Unos gostiju je zatvoren"}, status=403)

            tag_prefix = f"{sponsor.slug} "
            if sponsor.guestCap is not None and sponsor.guestCap > 0:
                count = Guests.objects.filter(tag__istartswith=tag_prefix).count()
                if count >= sponsor.guestCap:
                    return Response({"detail": "Guest limit reached"}, status=409)

            tag = f"{sponsor.slug} VIP - Sponzor - {sponsor.name}"

            guest = Guests.objects.create(
                name=name,
                tag=tag,
                bought=True,
                entered=False,
            )

        return Response(
            {"id": guest.id, "name": guest.name, "tag": guest.tag},
            status=status.HTTP_201_CREATED,
        )

    @transaction.atomic
    def perform_create(self, serializer):
        """
        When creating a Sponsor:
        - Take the current max `order`, increment by 1.
        - Generate a new UUID slug.
        """
        last = Sponsors.objects.select_for_update().order_by('-order').first()
        next_order = (last.order if last else 0) + 1
        serializer.save(order=next_order, slug=str(uuid4()), access_token=str(uuid4()))

    @action(detail=False, methods=['post'])
    @transaction.atomic
    def reorder(self, request):
        """
        Reorder sponsors by posting a list of {id, order}.
        Example payload:
        [
          { "id": 3, "order": 0 },
          { "id": 7, "order": 1 }
        ]
        """
        payload = request.data
        if not isinstance(payload, list):
            return Response(
                {"error": "Expected a list of {id, order}."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            pairs = [(int(item["id"]), int(item["order"])) for item in payload]
        except (KeyError, TypeError, ValueError):
            return Response(
                {"error": "Each item must have integer 'id' and 'order'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ids = [i for i, _ in pairs]
        orders = [o for _, o in pairs]

        if len(set(ids)) != len(ids):
            return Response({"error": "Duplicate ids in payload."}, status=status.HTTP_400_BAD_REQUEST)
        if len(set(orders)) != len(orders):
            return Response({"error": "Duplicate orders in payload."}, status=status.HTTP_400_BAD_REQUEST)
        if any(o < 0 for o in orders):
            return Response({"error": "Order must be non-negative integers."}, status=status.HTTP_400_BAD_REQUEST)

        objs = {obj.id: obj for obj in Sponsors.objects.select_for_update().filter(id__in=ids)}
        missing = sorted(set(ids) - set(objs.keys()))
        if missing:
            return Response({"error": f"Sponsor(s) not found: {missing}"}, status=status.HTTP_404_NOT_FOUND)

        for _id, _ord in pairs:
            objs[_id].order = _ord
        Sponsors.objects.bulk_update(objs.values(), ['order'])

        return Response({"status": "ok"}, status=status.HTTP_200_OK)

class PublicSponsorsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicSponsorsSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_queryset(self):
        return Sponsors.objects.filter(visible=True).order_by('order')

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [HasRole(Role.ADMIN)]


class CjenikViewSet(viewsets.ModelViewSet):
    queryset = Cjenik.objects.all()
    serializer_class = CjenikSerializer
    permission_classes = [ReadOnlyOrRole(Role.ADMIN)]

    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['tag']
    ordering_fields = ['order']


@method_decorator(never_cache, name="dispatch")
class VisibilityViewSet(viewsets.ModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer

    filter_backends = [DynamicSearchFilter]
    search_fields = ['name']

    permission_classes = [ReadOnlyOrRole(Role.ADMIN)]


class TranslationsViewSet(viewsets.ModelViewSet):
    queryset = Translations.objects.all()
    serializer_class = TranslationsSerializer

    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['key']
    ordering_fields = ['key']

    permission_classes = [ReadOnlyOrRole(Role.ADMIN)]

class LeaderboardPermission(BasePermission):
    """
    Allow anyone to GET or POST (read scores, submit scores).
    Require privilege for PUT, PATCH, DELETE.
    """
    def has_permission(self, request, view):
        if request.method in ('GET', 'POST', 'HEAD', 'OPTIONS'):
            return True
        return _caller_role(request) == Role.ADMIN

class GameLeaderboardViewSet(viewsets.ModelViewSet):
    queryset = GameLeaderboard.objects.all()
    serializer_class = GameLeaderboardSerializer
    permission_classes = [LeaderboardPermission]

    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['email']
    ordering_fields = ['score']


class BrucosiFormResponseViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    """Anyone can submit the form (throttled); only guest roles can read submissions."""
    queryset = BrucosiFormResponse.objects.all()
    serializer_class = BrucosiFormResponseSerializer
    permission_classes = [HasRole(*GUEST_ROLES)]

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def get_throttles(self):
        if self.action == 'create':
            return [FormThrottle()]
        return super().get_throttles()

class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]
            if not idinfo.get("email_verified"):
                return Response({"error": "Email not verified."}, status=status.HTTP_403_FORBIDDEN)
            if idinfo.get("hd") != "kset.org" or not email.endswith("@kset.org"):
                return Response({"error": "Unauthorized domain."}, status=status.HTTP_403_FORBIDDEN)

            name = idinfo.get("name", "")

            custom_user, created = Users.objects.get_or_create(
                email=email,
                defaults={"name": name, "privilege": Role.NONE}
            )
            if not created and not custom_user.name:
                custom_user.name = name
                custom_user.save()

            auth_user, _ = DjangoUser.objects.get_or_create(username=email, defaults={"email": email})
            if not auth_user.first_name:
                auth_user.first_name = name
                auth_user.save()

            refresh = RefreshToken.for_user(auth_user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": custom_user.id,
                    "name": custom_user.name,
                    "email": custom_user.email,
                    "privilege": custom_user.privilege,
                }
            })

        except Exception:
            return Response({"error": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    """GET /api/me/ — the caller's email, name and role ('none' if no Users row)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = Users.objects.get(email=request.user.username)
            return Response({
                "email": user.email,
                "name": user.name,
                "role": user.privilege,
            })
        except Users.DoesNotExist:
            return Response({
                "email": request.user.username,
                "name": "",
                "role": "none",
            })

SOFT_BOUNCE_REASON = 'mail se vratio (privremena greška)'
BREVO_BOUNCE_REASONS = {
    'hard_bounce': 'mail se vratio (trajna greška)',
    'soft_bounce': SOFT_BOUNCE_REASON,
    'blocked': 'mail blokiran',
    'invalid_email': 'neispravna adresa',
    'error': 'greška pri isporuci',
}


class BrevoWebhookView(APIView):
    """POST /api/brevo/webhook/<token>/ — Brevo transactional events; flags bounced ticket mails."""
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, token):
        expected = settings.BREVO_WEBHOOK_TOKEN
        if not expected or not hmac.compare_digest(token.encode(), expected.encode()):
            return Response(status=status.HTTP_404_NOT_FOUND)

        events = request.data if isinstance(request.data, list) else [request.data]
        for event in events:
            if not isinstance(event, dict):
                continue
            message_id = str(event.get('message-id') or '').strip().strip('<>')

            if event.get('event') == 'delivered':
                if message_id:
                    Guests.objects.filter(
                        Q(mailStatus='sent') | Q(mailStatus='bounced', mailError=SOFT_BOUNCE_REASON),
                        mailMessageId=f'<{message_id}>',
                    ).update(mailStatus='delivered', mailError='')
                continue

            reason = BREVO_BOUNCE_REASONS.get(event.get('event'))
            if not reason:
                continue

            email = str(event.get('email') or '').strip()
            if message_id:
                guests = Guests.objects.filter(mailMessageId=f'<{message_id}>')
            elif email:
                guests = Guests.objects.filter(email__iexact=email, bought=True)
            else:
                continue
            guests.update(mailStatus='bounced', mailError=reason)

        return Response({"status": "ok"})


def _db_models():
    return {
        m._meta.db_table: m
        for m in apps.get_models()
        if m._meta.db_table.startswith('bruc_')
    }


@method_decorator(never_cache, name='dispatch')
class DbTablesView(APIView):
    """GET /api/db/tables/ — every bruc_* table with its row count."""
    permission_classes = [IsAuthenticated, HasRole(Role.ADMIN)]

    def get(self, request):
        tables = [
            {
                "table": table,
                "label": f"{model._meta.app_label}.{model.__name__}",
                "count": model.objects.count(),
            }
            for table, model in sorted(_db_models().items())
        ]
        return Response(tables)


@method_decorator(never_cache, name='dispatch')
class DbTableRowsView(APIView):
    """GET /api/db/tables/<table>/ — read-only dump of one table (capped)."""
    permission_classes = [IsAuthenticated, HasRole(Role.ADMIN)]

    def get(self, request, table):
        model = _db_models().get(table)
        if model is None:
            return Response({"error": "Unknown table."}, status=status.HTTP_404_NOT_FOUND)

        columns = [f.attname for f in model._meta.concrete_fields]
        rows = list(model.objects.order_by('pk').values(*columns)[:MAX_BULK_RECORDS])
        total = model.objects.count()
        return Response({
            "table": table,
            "columns": columns,
            "pk": model._meta.pk.attname,
            "rows": rows,
            "total": total,
            "truncated": total > len(rows),
        })
