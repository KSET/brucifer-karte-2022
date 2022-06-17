import imp
from django.contrib import admin

from .models import Guests, Tags, Users

admin.site.register(Guests)
admin.site.register(Tags)
admin.site.register(Users)
