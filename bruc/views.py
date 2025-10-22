from uuid import uuid4
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import filters
from rest_framework import routers, serializers, viewsets
from .models import Translations, Visibility, Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact, Mailer, GameLeaderboard, BrucosiFormResponse
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import BrucosiFormResponseSerializer, TranslationsSerializer, VisibilitySerializer, CjenikSerializer, GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer, DynamicSearchFilter, MailerSerializer, GameLeaderboardSerializer, PublicLineupSerializer, PublicSponsorsSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import action
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
import json
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from rest_framework.decorators import action
from rest_framework import viewsets

from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from django.contrib.auth.models import User as DjangoUser

from datetime import datetime, time
from django.utils.timezone import make_aware

class MailerViewSet(viewsets.ModelViewSet):
    queryset = Mailer.objects.all()
    serializer_class = MailerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def send_mail(self, request):
        emails = request.data.get('emails', [])  # Expecting a list of email details

        messages = []
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
                html_message = render_to_string('emails/guest_email.html', {
                    'name': email.get('name', ''), 'confCode': email.get('confCode', ''),
                    'qrSrc': "https://api.qrserver.com/v1/create-qr-code/?data="+email.get('confCode', '')+"&amp;size=300x300"})
            elif template_name == "sponsors_email":
                html_message = render_to_string('emails/sponsors_email.html', {
                    'name': email.get('name', ''), 'link': email.get('link', '')})

            if subject and msg and to and html_message:
                text_content = strip_tags(html_message)
                msg = EmailMultiAlternatives(subject, text_content, "42. Brucošijada FER-a<"+settings.EMAIL_HOST_USER+">", [to])
                msg.attach_alternative(html_message, "text/html")
                messages.append(msg)

        if messages:
            try:
                for msg in messages:
                    msg.send()
                return HttpResponse('Emails sent successfully.')
            except Exception as e:
                return HttpResponse(f'An error occurred: {str(e)}')
        else:
            return HttpResponse('Make sure all fields are entered and valid for each email.')


class GuestsViewSet(viewsets.ModelViewSet):
    queryset = Guests.objects.all()
    serializer_class = GuestsSerializer
    filter_backends = [DynamicSearchFilter]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='bulk-import')
    def bulk_import(self, request):
        guests_data = json.loads(request.body)
        guests_serializer = GuestsSerializer(data=guests_data, many=True)  # 'many=True' is important for bulk operations
        
        if guests_serializer.is_valid():
            # Using atomic transactions to ensure all-or-nothing
            with transaction.atomic():
                Guests.objects.bulk_create([Guests(**data) for data in guests_serializer.validated_data])
                return Response({'message': 'Bulk guests import successful'}, status=status.HTTP_201_CREATED)
            
    @action(detail=False, methods=['get'], url_path='search-brucosi')
    def search_brucosi(self, request):
        jmbag = request.query_params.get('jmbag')
        if not jmbag:
            return Response({"error": "Missing jmbag parameter"}, status=status.HTTP_400_BAD_REQUEST)

        guests = Guests.objects.filter(jmbag__icontains=jmbag, tag="Brucoši")
        submissions = BrucosiFormResponse.objects.filter(jmbag__icontains=jmbag)

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
            "guests": guest_data,
            "submissions": submission_data
        })
    
    @action(detail=False, methods=["get"], url_path="today-stats")
    def today_stats(self, request):
        now = datetime.now()
        today_start = make_aware(datetime.combine(now.date(), time.min))
        noon_time = make_aware(datetime.combine(now.date(), time(12, 0)))
        today_end = make_aware(datetime.combine(now.date(), time.max))

        guests = Guests.objects.filter(
            boughtTicketTime__range=(today_start, today_end)
        )

        total_entries = guests.count()
        tickets_before_12 = guests.filter(boughtTicketTime__lt=noon_time).count()
        tickets_after_12 = guests.filter(boughtTicketTime__gte=noon_time).count()

        return Response({
            "date": now.date().isoformat(),
            "totalEntries": total_entries,
            "ticketsBefore12": tickets_before_12,
            "ticketsAfter12": tickets_after_12,
        })

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='bulk-import')
    def bulk_import(self, request):
        user_data = json.loads(request.body)
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
    ordering_fields = ['order']
    permission_classes = [IsAuthenticated]

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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_queryset(self):
        return Lineup.objects.filter(visible=True).order_by('order')

class SponsorsViewSet(viewsets.ModelViewSet):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer
    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    ordering_fields = ['order']
    permission_classes = [IsAuthenticated]

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

    @action(
        detail=False,
        methods=['get', 'post', 'delete'],
        permission_classes=[AllowAny],
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
            if not slug:
                return Response({"detail": "slug is required"}, status=400)

            sponsor = Sponsors.objects.filter(slug=slug, visible=True).first()
            if not sponsor:
                return Response({"detail": "Sponsor not found"}, status=404)

            tag_prefix = f"{sponsor.slug} "
            qs = Guests.objects.filter(tag__istartswith=tag_prefix).order_by("id")

            return Response(
                GuestsSerializer(qs, many=True).data,
                status=200,
            )

        # ------------------ DELETE ------------------
        if request.method == 'DELETE':
            slug = (request.query_params.get("slug") or "").strip()
            guest_id = (request.query_params.get("id") or "").strip()

            if not slug or not guest_id:
                return Response({"detail": "slug and id are required"}, status=400)

            sponsor = Sponsors.objects.filter(slug=slug).first()
            if not sponsor:
                return Response({"detail": "Sponsor not found"}, status=404)

            guest = Guests.objects.filter(id=guest_id, tag__icontains=sponsor.slug).first()
            if not guest:
                return Response({"detail": "Guest not found"}, status=404)

            guest.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # ------------------ POST ------------------
        slug = (request.data.get("slug") or "").strip()
        name = (request.data.get("name") or "").strip()

        if not slug or not name:
            return Response({"detail": "slug and name are required"}, status=400)

        sponsor = Sponsors.objects.filter(slug=slug).first()
        if not sponsor:
            return Response({"detail": "Sponsor not found"}, status=404)

        if getattr(sponsor, "guestCap", None) is not None:
            count = Guests.objects.filter(tag__icontains=sponsor.slug).count()
            if count >= int(sponsor.guestCap):
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

class PublicSponsorsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicSponsorsSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_queryset(self):
        return Sponsors.objects.filter(visible=True).order_by('order')

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]


class CjenikViewSet(viewsets.ModelViewSet):
    queryset = Cjenik.objects.all()
    serializer_class = CjenikSerializer

    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['tag']
    ordering_fields = ['order']


class VisibilityViewSet(viewsets.ModelViewSet):
    queryset = Visibility.objects.all()
    serializer_class = VisibilitySerializer

    filter_backends = [DynamicSearchFilter]
    search_fields = ['name']


class TranslationsViewSet(viewsets.ModelViewSet):
    queryset = Translations.objects.all()
    serializer_class = TranslationsSerializer

    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['key']
    ordering_fields = ['key']

class GameLeaderboardViewSet(viewsets.ModelViewSet):
    queryset = GameLeaderboard.objects.all()
    serializer_class = GameLeaderboardSerializer

    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    search_fields = ['email']
    ordering_fields = ['score']

class AllowPostAnyOtherwiseAuthenticated(BasePermission):
    """
    Allow anyone to POST.
    Require authentication for all other methods.
    """
    def has_permission(self, request, view):
        if request.method in ("POST"):
            return True
        return bool(request.user and request.user.is_authenticated)

class BrucosiFormResponseViewSet(viewsets.ModelViewSet):
    queryset = BrucosiFormResponse.objects.all()
    serializer_class = BrucosiFormResponseSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='brucosi-form-submit')
    def brucosi_form_submit(self, request):
        serializer = BrucosiFormResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Submission received."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            name = idinfo.get("name", "")

            custom_user, created = Users.objects.get_or_create(
                email=email,
                defaults={"name": name, "privilege": "0"}
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

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)