from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import filters
from rest_framework import routers, serializers, viewsets
from .models import Guests, Tags, Users, Lineup, Sponsors, Contact,Mailer
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer,DynamicSearchFilter, MailerSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.decorators import action


# Create your views here.
class MailerViewSet(viewsets.ModelViewSet):
    queryset = Mailer.objects.all()
    serializer_class = MailerSerializer

    @action(detail=True, methods=['post'])
    def send_mail(self,request,pk):  
        print(request.data.get('subject', ''))
        subject = request.data.get('subject', '')
        msg = request.data.get('message', '')
        to = request.data.get('to_mail', '')
        
        if subject and msg and settings.EMAIL_HOST_USER:
            try:
                send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')

class GuestsViewSet(viewsets.ModelViewSet):
    queryset = Guests.objects.all()
    serializer_class = GuestsSerializer
    filter_backends = [DynamicSearchFilter]

    '''def send_mail(request):  
        subject = request.POST.get('subject', '')
        msg = request.POST.get('message', '')
        to = request.POST.get('to_mail', '')
        
        if subject and msg and settings.EMAIL_HOST_USER:
            try:
                send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            # In reality we'd use a form class
            # to get proper validation errors.
            return HttpResponse('Make sure all fields are entered and valid.')'''

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
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]


    search_fields = ['slug']
    ordering_fields = ['order']


class SponsorsViewSet(viewsets.ModelViewSet):
    queryset = Sponsors.objects.all()
    serializer_class = SponsorsSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]

    search_fields = ['slug']
    ordering_fields = ['order']

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    
