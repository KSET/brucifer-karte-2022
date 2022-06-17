from socket import if_indextoname
from rest_framework import serializers, filters
from .models import Guests, Tags, Users

class GuestsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guests
        fields = ["id","name","surname","phone","tag","bought","entered","deleted"]


class TagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tags
        fields = ["id","name","count","bought","entered"]


class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ["id","name","email","privilege"]
     

class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])




