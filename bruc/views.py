from uuid import uuid4
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import filters
from rest_framework import routers, serializers, viewsets
from .models import Translations, Visibility, Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact, Mailer, GameLeaderboard, BrucosiFormResponse
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import BrucosiFormResponseSerializer, TranslationsSerializer, VisibilitySerializer, CjenikSerializer, GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer, DynamicSearchFilter, MailerSerializer, GameLeaderboardSerializer
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

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [IsAuthenticated]


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    permission_classes = [AllowAny]

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


class SponsorsViewSet(viewsets.ModelViewSet):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer
    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    ordering_fields = ['order']


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
        if request.method in ("POST", "GET"):
            return True
        return bool(request.user and request.user.is_authenticated)

class BrucosiFormResponseViewSet(viewsets.ModelViewSet):
    queryset = BrucosiFormResponse.objects.all()
    serializer_class = BrucosiFormResponseSerializer
    permission_classes = [AllowPostAnyOtherwiseAuthenticated]

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