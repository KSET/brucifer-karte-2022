from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import filters
from rest_framework import routers, serializers, viewsets
from .models import Guests, Tags, Users, Lineup, Sponsors, Contact
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import GuestsSerializer, TagsSerializer, UsersSerializer, LineupSerializer, SponsorsSerializer, ContactSerializer,DynamicSearchFilter
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

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
    
    
def my_mail(request):  
    subject = request.POST.get('subject', '')
    msg = request.POST.get('message', '')
    to = request.POST.get('to_mail', '')
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])  
    if(res == 1):  
        msg = "Mail Sent Successfully."  
    else:  
        msg = "Mail Sending Failed."  
    return HttpResponse(msg)  