import hmac
import json
from datetime import datetime, time, timedelta
from uuid import uuid4

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.core.mail import EmailMultiAlternatives, get_connection
from django.db import DatabaseError, transaction
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.utils.timezone import make_aware
from django.views.decorators.cache import never_cache
from django_filters.rest_framework import DjangoFilterBackend
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, SimpleRateThrottle
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .auth import RequireXHRHeader, blacklist_refresh_cookie, clear_refresh_cookie, set_refresh_cookie
from .models import Translations, Visibility, Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact, Mailer, GameLeaderboard, BrucosiFormResponse
from .roles import Role, GUEST_ROLES
from .search import LONG, fold, name_rank, name_search_q
from .serializer import BrucosiFormResponseSerializer, TranslationsSerializer, VisibilitySerializer, CjenikSerializer, GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer, DynamicSearchFilter, MailerSerializer, GameLeaderboardSerializer, PublicLineupSerializer, PublicSponsorsSerializer, SponsorGuestSerializer, SponsorPortalSerializer
from .services import (
    SponsorGuestCapReached, SponsorGuestEntered, SponsorInputClosed, add_sponsor_guest, delete_sponsor_guest, derive_fer_email,
    send_guest_ticket_email, send_guest_ticket_email_async, sponsor_portal_link, update_sponsor_guest,
)

class SponsorPortalTokenThrottle(SimpleRateThrottle):
    # Per link, so colleagues behind one office NAT share a budget only with their own sponsor.
    # One request per add/edit/delete; a sponsor entering a long list must not get locked out.
    scope = 'sponsor_portal'
    rate = '600/hour'

    def get_cache_key(self, request, view):
        # Unknown tokens get no bucket of their own (the IP throttle still applies), so random URLs can't fill the cache.
        if view.sponsor is None:
            return None
        return self.cache_format % {'scope': self.scope, 'ident': view.sponsor.pk}


class SponsorPortalIPThrottle(AnonRateThrottle):
    # Loose flood guard across tokens; links are 256-bit, so guessing isn't what this protects against.
    scope = 'sponsor_portal_ip'
    rate = '1000/hour'

class MailerThrottle(AnonRateThrottle):
    rate = '200/hour'

class FormThrottle(AnonRateThrottle):
    # Loose per-IP flood guard: freshmen on FER eduroam share one public IP.
    rate = '1000/hour'


class LoginThrottle(AnonRateThrottle):
    scope = 'auth_login'
    rate = '30/minute'


class RefreshThrottle(AnonRateThrottle):
    # Every open tab refreshes, and entry staff at an event share one venue IP.
    scope = 'auth_refresh'
    rate = '120/minute'


class FormJmbagThrottle(SimpleRateThrottle):
    scope = 'form_jmbag'
    rate = '5/hour'

    def get_cache_key(self, request, view):
        # Keyed per IP too, so nobody can lock a student out by spamming their JMBAG from elsewhere.
        data = request.data if isinstance(request.data, dict) else {}
        jmbag = str(data.get('jmbag') or '').strip()
        if not jmbag:
            return None
        return self.cache_format % {'scope': self.scope, 'ident': f'{self.get_ident(request)}:{jmbag}'}


MAX_BULK_RECORDS = 5000
FAILED_MAIL_STATUSES = ('failed', 'bounced')
STALE_PENDING_MAIL = timedelta(minutes=5)


def _failed_mail_q():
    """Failed or bounced mails, plus background sends that never finished (e.g. server restart)."""
    return Q(mailStatus__in=FAILED_MAIL_STATUSES) | Q(
        mailStatus='pending', boughtTicketTime__lt=timezone.now() - STALE_PENDING_MAIL)


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
                link = sponsor_portal_link(sponsor)
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
    filterset_fields = {'bought': ['exact'], 'entered': ['exact'], 'tag': ['icontains']}
    permission_classes = [HasRole(*GUEST_ROLES)]
    MAX_LIMIT = 200
    MAX_TERMS = 10

    def filter_queryset(self, queryset):
        """Entry search: ?name_search= ignores diacritics in name and surname, and ?limit=N returns
        only the N best matches; without them the full list is returned."""
        queryset = super().filter_queryset(queryset)
        if self.action != 'list':
            return queryset
        params = self.request.query_params
        terms = params.get('name_search', '').split()[:self.MAX_TERMS]
        if terms:
            queryset = queryset.filter(name_search_q(terms))
        if 'limit' not in params:
            return queryset
        try:
            limit = int(params['limit'])
        except ValueError:
            limit = 0
        if not 1 <= limit <= self.MAX_LIMIT:
            raise ValidationError({'limit': f'Mora biti broj od 1 do {self.MAX_LIMIT}.'})
        return queryset.annotate(rank=name_rank(terms)).order_by('-rank', 'searchKey', 'id')[:limit]

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
            "failedMails": brucosi.filter(_failed_mail_q(), bought=True).count(),
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
                mailStatus='pending', mailError='', mailSentAt=None, mailMessageId='')
            if not claimed:
                return Response({"detail": "Karta je već prodana."}, status=status.HTTP_409_CONFLICT)
            BrucosiFormResponse.objects.filter(jmbag=guest.jmbag).update(status='redeemed')

        guest.refresh_from_db()
        send_guest_ticket_email_async(guest.pk)
        return Response({"guest": GuestsSerializer(guest).data, "email": email})

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
            BrucosiFormResponse.objects.filter(jmbag=guest.jmbag).update(status='pending')
        guest.refresh_from_db()
        return Response({"guest": GuestsSerializer(guest).data})

    @action(detail=True, methods=['post'], url_path='check-in',
            permission_classes=[HasRole(Role.ENTRY, Role.ENTRY_TICKETS, Role.ADMIN)])
    def check_in(self, request, pk=None):
        guest = self.get_object()
        checked_in = Guests.objects.filter(pk=guest.pk, entered=False).update(entered=True)
        guest.refresh_from_db()
        data = GuestsSerializer(guest).data
        if not checked_in:
            return Response({"detail": "Gost je već ušao.", "guest": data}, status=status.HTTP_409_CONFLICT)
        return Response({"guest": data})

    @action(detail=True, methods=['post'], url_path='undo-check-in',
            permission_classes=[HasRole(Role.ENTRY, Role.ENTRY_TICKETS, Role.ADMIN)])
    def undo_check_in(self, request, pk=None):
        guest = self.get_object()
        Guests.objects.filter(pk=guest.pk).update(entered=False)
        guest.refresh_from_db()
        return Response({"guest": GuestsSerializer(guest).data})

    @action(detail=True, methods=['post'], url_path='resend-mail', permission_classes=[HasRole(Role.ADMIN)])
    def resend_mail(self, request, pk=None):
        guest = self.get_object()
        if not guest.bought or not guest.confCode:
            return Response({"detail": "Karta nije prodana."}, status=status.HTTP_400_BAD_REQUEST)
        if guest.mailStatus == 'pending' and not Guests.objects.filter(_failed_mail_q(), pk=guest.pk).exists():
            return Response({"detail": "Mail se još šalje, pričekajte."}, status=status.HTTP_409_CONFLICT)

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
        guests = Guests.objects.filter(_failed_mail_q(), bought=True).order_by('-boughtTicketTime')
        return Response(GuestsSerializer(guests, many=True).data)

def guest_stats(q):
    return Guests.objects.filter(q).aggregate(
        count=Count('id'),
        bought=Count('id', filter=Q(bought=True)),
        entered=Count('id', filter=Q(entered=True)),
    )


def tag_parents(tags):
    """A tag's parent is the longest other tag whose name it contains (vip-sponzor goes under vip).
    Tags with the same name can't contain each other, so there are no cycles."""
    parents = {}
    for tag in tags:
        name = tag.name.casefold()
        candidates = [other for other in tags
                      if other.name and other.name.casefold() != name and other.name.casefold() in name]
        parents[tag.id] = max(candidates, key=lambda other: len(other.name), default=None)
    return parents


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [ReadOnlyOrRole(Role.ADMIN, read_roles=GUEST_ROLES)]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Guest counts per tag as a tree: each child is listed right after its parent. A guest's tag matches
        every tag contained in it, so a parent's count already includes its children, and the totals count
        each guest once instead of summing the rows."""
        # alphabetical ignoring case and accents, so Č sorts with C instead of after Z
        tags = sorted(self.get_queryset(), key=lambda tag: (fold(tag.name, LONG), tag.name))
        parents = tag_parents(tags)
        children = {}
        for tag in tags:
            children.setdefault(parents[tag.id] and parents[tag.id].id, []).append(tag)

        rows = []

        def add(parent_id, depth):
            for tag in children.get(parent_id, []):
                parent = parents[tag.id]
                rows.append({'id': tag.id, 'name': tag.name, 'parent': parent and parent.name, 'depth': depth,
                             **guest_stats(Q(tag__icontains=tag.name))})
                add(tag.id, depth + 1)

        add(None, 0)
        any_tag = Q()
        for tag in tags:
            any_tag |= Q(tag__icontains=tag.name)
        totals = guest_stats(any_tag) if tags else {'count': 0, 'bought': 0, 'entered': 0}
        return Response({'tags': rows, 'totals': totals})


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [DynamicSearchFilter]
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

    def get_queryset(self):
        return Sponsors.objects.annotate(
            guestsAdded=Count('guests'),
            guestsEntered=Count('guests', filter=Q(guests__entered=True)),
        )

    @transaction.atomic
    def perform_create(self, serializer):
        """
        When creating a Sponsor:
        - Take the current max `order`, increment by 1.
        - Generate a new UUID slug (the access token gets its own default).
        """
        last = Sponsors.objects.select_for_update().order_by('-order').first()
        next_order = (last.order if last else 0) + 1
        serializer.save(order=next_order, slug=str(uuid4()))

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

class SponsorPortalMixin:
    """Public sponsor guest list, authenticated by the secret token in the URL."""
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [SponsorPortalTokenThrottle, SponsorPortalIPThrottle]

    def initial(self, request, *args, **kwargs):
        # Resolved before throttling so the per-token throttle can key on real sponsors only.
        # `visible` only controls the public sponsors page; new sponsors are hidden by default but get invited.
        self.sponsor = Sponsors.objects.filter(access_token=kwargs.get('token', '')).first()
        super().initial(request, *args, **kwargs)

    def get_sponsor(self):
        if self.sponsor is None:
            raise NotFound()
        return self.sponsor

    def run_guarded(self, fn):
        try:
            return fn()
        except (Guests.DoesNotExist, Sponsors.DoesNotExist):
            raise NotFound()
        except SponsorInputClosed:
            return Response({"detail": "Unos gostiju je zatvoren."}, status=status.HTTP_403_FORBIDDEN)
        except SponsorGuestCapReached:
            return Response({"detail": "Unijeli ste maksimalan broj gostiju."}, status=status.HTTP_409_CONFLICT)
        except SponsorGuestEntered:
            return Response({"detail": "Gost je već ušao i ne može se mijenjati."}, status=status.HTTP_409_CONFLICT)


class SponsorPortalView(SponsorPortalMixin, APIView):
    def get(self, request, token):
        sponsor = self.get_sponsor()
        return Response(SponsorPortalSerializer(sponsor, context={'request': request}).data)


class SponsorPortalGuestsView(SponsorPortalMixin, APIView):
    def post(self, request, token):
        sponsor = self.get_sponsor()
        serializer = SponsorGuestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        def create():
            guest = add_sponsor_guest(sponsor, **serializer.validated_data)
            return Response(SponsorGuestSerializer(guest).data, status=status.HTTP_201_CREATED)
        return self.run_guarded(create)


class SponsorPortalGuestDetailView(SponsorPortalMixin, APIView):
    def patch(self, request, token, guest_id):
        sponsor = self.get_sponsor()
        serializer = SponsorGuestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        def update():
            guest = update_sponsor_guest(sponsor, guest_id, **serializer.validated_data)
            return Response(SponsorGuestSerializer(guest).data)
        return self.run_guarded(update)

    def delete(self, request, token, guest_id):
        sponsor = self.get_sponsor()

        def remove():
            delete_sponsor_guest(sponsor, guest_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return self.run_guarded(remove)


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


class BrucosiFormResponseViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Anyone can submit the form (throttled). Submissions are read only through search-brucosi."""
    queryset = BrucosiFormResponse.objects.all()
    serializer_class = BrucosiFormResponseSerializer
    permission_classes = [AllowAny]
    throttle_classes = [FormThrottle, FormJmbagThrottle]

class GoogleAuthView(APIView):
    """POST /api/auth/google/ — exchanges a Google ID token for an access token + refresh cookie."""
    # sets the refresh cookie, so it gets the same CSRF guard as refresh/logout; JSON-only rules out plain form posts
    permission_classes = [RequireXHRHeader]
    authentication_classes = []
    parser_classes = [JSONParser]
    throttle_classes = [LoginThrottle]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        except (ValueError, GoogleAuthError):
            return Response({"error": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)

        email = idinfo.get("email", "")
        if not idinfo.get("email_verified"):
            return Response({"error": "Email not verified."}, status=status.HTTP_403_FORBIDDEN)

        name = idinfo.get("name", "")

        try:
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

            if not auth_user.is_active or custom_user.privilege == Role.NONE:
                return Response({"error": "No privileges.", "code": "no_privileges"}, status=status.HTTP_403_FORBIDDEN)

            blacklist_refresh_cookie(request)
            refresh = RefreshToken.for_user(auth_user)
        except DatabaseError:
            return Response({"error": "Authentication failed."}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({
            "access": str(refresh.access_token),
            "user": _user_payload(custom_user),
        })
        set_refresh_cookie(response, refresh)
        return response


def _user_payload(user):
    return {
        "name": user.name,
        "email": user.email,
        "role": user.privilege,
    }


def _privileged_user(refresh):
    """The token owner's (auth user, Users row), or None when they were deactivated, removed from Users or demoted to Role.NONE."""
    auth_user = DjangoUser.objects.filter(pk=refresh[jwt_settings.USER_ID_CLAIM], is_active=True).first()
    if auth_user is None:
        return None
    user = Users.objects.filter(email=auth_user.username).exclude(privilege=Role.NONE).first()
    return (auth_user, user) if user else None


def _revoked_session_response(refresh):
    refresh.blacklist()
    response = Response({"error": "No privileges."}, status=status.HTTP_401_UNAUTHORIZED)
    clear_refresh_cookie(response)
    return response


class CookieTokenRefreshView(APIView):
    """POST /api/auth/token/refresh/ — reads the refresh cookie, returns a new access token + the user, rotates the cookie."""
    permission_classes = [RequireXHRHeader]
    authentication_classes = []
    throttle_classes = [RefreshThrottle]

    def post(self, request):
        try:
            refresh = RefreshToken(request.COOKIES.get(settings.AUTH_REFRESH_COOKIE, ""))
        except TokenError:
            return Response({"error": "Session expired."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            owner = _privileged_user(refresh)
            if owner is None:
                return _revoked_session_response(refresh)
            auth_user, user = owner

            _, claimed = refresh.blacklist()
            if not claimed:
                return Response({"error": "Session expired."}, status=status.HTTP_401_UNAUTHORIZED)
            new_refresh = RefreshToken.for_user(auth_user)
        except DatabaseError:
            return Response({"error": "Try again later."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        response = Response({"access": str(new_refresh.access_token), "user": _user_payload(user)})
        set_refresh_cookie(response, new_refresh)
        return response


class LogoutView(APIView):
    """POST /api/auth/logout/ — revokes the refresh cookie's token and clears the cookie."""
    permission_classes = [RequireXHRHeader]
    authentication_classes = []

    def post(self, request):
        blacklist_refresh_cookie(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        clear_refresh_cookie(response)
        return response


class MeView(APIView):
    """GET /api/me/ — the caller's email, name and role ('none' if no Users row)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return Response(_user_payload(Users.objects.get(email=request.user.username)))
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
