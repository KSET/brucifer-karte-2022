import imp
from django.contrib import admin

from .models import Cjenik, Contact, Guests, Tags, Users, Lineup, Sponsors

admin.site.register(Guests)
admin.site.register(Tags)
admin.site.register(Users)
admin.site.register(Lineup)
admin.site.register(Sponsors)
admin.site.register(Contact)
admin.site.register(Cjenik)

