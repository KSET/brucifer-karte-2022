from socket import if_indextoname
from rest_framework import serializers, filters
from .models import Guests, Tags, Users, Lineup, Sponsors

class GuestsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guests
        fields = ["id","name","surname","jmbag","email","tag","bought","entered","confCode"]

class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ["id","name","count","bought","entered"]

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ["id","name","email","privilege"]
    
class LineupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lineup
        fields = ["id","slug","name","image"]

class SponsorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sponsors
        fields = ["id","slug","name","url","image","email","guestCap"]

class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])




