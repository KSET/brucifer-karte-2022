from socket import if_indextoname
from rest_framework import serializers, filters
from .models import Translations, Visibility, Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact, Mailer, GameLeaderboard


class GuestsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guests
        fields = ["id", "name", "surname", "jmbag",
                  "email", "tag", "bought", "entered", "confCode", "boughtTicketTime"]


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "name", "count", "bought", "entered"]


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "name", "email", "privilege"]


class LineupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lineup
        fields = ["id", "slug", "order", "visible", "name", "image"]


class SponsorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sponsors
        fields = ["id", "slug", "order", "visible", "guestsEnabled",
                  "name", "url", "image", "email", "guestCap"]


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "bandName", "bookerName", "bookerPhone"]


class MailerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Mailer
        fields = ["subject", "message", "to_mail"]


class CjenikSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cjenik
        fields = ["id", "name", "tag", "order", "priceEUR", "volume"]


class VisibilitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visibility
        fields = ["name", "visible"]


class TranslationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Translations
        fields = ["id", "key", "value"]

class GameLeaderboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameLeaderboard
        fields = ["id", "name", "email", "score"]


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])
