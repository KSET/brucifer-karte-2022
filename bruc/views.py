from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import filters
from rest_framework import routers, serializers, viewsets
from .models import Guests, Tags, Users
from django_filters.rest_framework import DjangoFilterBackend
from .serializer import GuestsSerializer, TagsSerializer, UsersSerializer, DynamicSearchFilter

# Create your views here.

class GuestsViewSet(viewsets.ModelViewSet):
    queryset = Guests.objects.all()
    serializer_class = GuestsSerializer
    #filterset_fields = ['bought','tag']
    filter_backends = [DynamicSearchFilter]
    #search_fields = ['name', 'surname']
    

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']













def home(request):
    return render(request,'home.html')

def guests(request):
    return render(request,'guests.html')

def tags(request):
    return render(request,'tags.html')

def privileges(request):
    return render(request,'privileges.html')
    
def users(request):
    return render(request,'users.html')
    
def iimport(request):
    return render(request,'iimport.html')
    
def export(request):
    return render(request,'export.html')
    
def logout(request):
    return render(request,'logout.html')

def login(request):
    return render(request,'login.html')
    
    