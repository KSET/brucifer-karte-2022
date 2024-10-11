from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import filters
from rest_framework import routers, serializers, viewsets
from .models import Translations, Visibility, Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact, Mailer, GameLeaderboard
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import TranslationsSerializer, VisibilitySerializer, CjenikSerializer, GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer, DynamicSearchFilter, MailerSerializer, GameLeaderboardSerializer
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

# Create your views here.



class MailerViewSet(viewsets.ModelViewSet):
    queryset = Mailer.objects.all()
    serializer_class = MailerSerializer

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
                msg = EmailMultiAlternatives(subject, text_content, "41. Brucošijada FER-a<"+settings.EMAIL_HOST_USER+">", [to])
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

    @action(detail=False, methods=['post'], url_path='bulk-import')
    def bulk_import(self, request):
        guests_data = json.loads(request.body)
        guests_serializer = GuestsSerializer(data=guests_data, many=True)  # 'many=True' is important for bulk operations
        
        if guests_serializer.is_valid():
            # Using atomic transactions to ensure all-or-nothing
            with transaction.atomic():
                Guests.objects.bulk_create([Guests(**data) for data in guests_serializer.validated_data])
                return Response({'message': 'Bulk guests import successful'}, status=status.HTTP_201_CREATED)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

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


class SponsorsViewSet(viewsets.ModelViewSet):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer
    filter_backends = [DynamicSearchFilter, filters.OrderingFilter]
    ordering_fields = ['order']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


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
