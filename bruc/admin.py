import imp
from django.contrib import admin

from .models import GameLeaderboard, Translations, Visibility, Cjenik, Contact, Guests, Tags, Users, Lineup, Sponsors

admin.site.register(Guests)
admin.site.register(Tags)
admin.site.register(Users)
admin.site.register(Lineup)
admin.site.register(Sponsors)
admin.site.register(Contact)
admin.site.register(Cjenik)
admin.site.register(Visibility)
admin.site.register(Translations)
admin.site.register(GameLeaderboard)
