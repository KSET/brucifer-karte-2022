from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import filters
from rest_framework import routers, serializers, viewsets
from .models import Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact,Mailer
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import CjenikSerializer, GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer,DynamicSearchFilter, MailerSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import action
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
class MailerViewSet(viewsets.ModelViewSet):
    queryset = Mailer.objects.all()
    serializer_class = MailerSerializer

    @action(detail=True, methods=['post'])
    def send_mail(self,request,pk):  
        subject = request.data.get('subject', '')
        msg = request.data.get('message', '')
        to = request.data.get('to_mail', '')
        template_name = request.data.get('template', '')

        if(template_name=="user_email"):
            html_message = render_to_string('emails/user_email.html',{
            'name': request.data.get('name', ''), 'privilege_name': request.data.get('privilege_name', ''),})
        elif(template_name=="guest_email"):
            html_message = render_to_string('emails/guest_email.html',{
            'name': request.data.get('name', ''), 'confCode': request.data.get('confCode', '')})
        elif(template_name=="sponsors_email"):
            html_message = render_to_string('emails/sponsors_email.html',{
            'name': request.data.get('name', ''), 'link': request.data.get('link', '')})

        if subject and msg and settings.EMAIL_HOST_USER:
            try:
                send_mail(subject, msg, settings.EMAIL_HOST_USER, [to],fail_silently=True,html_message=html_message)
                x=1
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Passed')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

class GuestsViewSet(viewsets.ModelViewSet):
    queryset = Guests.objects.all()
    serializer_class = GuestsSerializer
    filter_backends = [DynamicSearchFilter]

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

class LineupViewSet(viewsets.ModelViewSet):
    queryset = Lineup.objects.all()
    serializer_class = LineupSerializer
    filter_backends = [DynamicSearchFilter,filters.OrderingFilter]
    ordering_fields = ['order']


class SponsorsViewSet(viewsets.ModelViewSet):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer
    filter_backends = [DynamicSearchFilter,filters.OrderingFilter]
    ordering_fields = ['order']

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class CjenikViewSet(viewsets.ModelViewSet):
    queryset = Cjenik.objects.all()
    serializer_class = CjenikSerializer

    filter_backends = [DynamicSearchFilter,filters.OrderingFilter]
    search_fields = ['tag']
    ordering_fields = ['order']
    
    
