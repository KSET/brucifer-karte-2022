import re
from rest_framework import serializers, filters
from .services import sponsor_input_state, sponsor_portal_link
from .models import SPONSOR_TAG_MARKER, Translations, Visibility, Cjenik, Guests, Tags, Users, Lineup, Sponsors, Contact, Mailer, GameLeaderboard, BrucosiFormResponse


class GuestsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Guests
        fields = ["id", "name", "surname", "jmbag",
                  "email", "tag", "bought", "entered", "confCode", "boughtTicketTime",
                  "mailStatus", "mailError", "mailSentAt"]
        read_only_fields = ["mailStatus", "mailError", "mailSentAt"]

    def validate(self, attrs):
        # guests.sponsor follows the tag, so admins can add/import sponsor guests as an override
        # (past cap or deadline) and moving a guest to another tag unlinks it.
        # Admin forms resend the unchanged tag on every edit, so compare trimmed (DRF strips it too).
        tag = attrs.get("tag")
        if tag is None or (self.instance is not None and tag == (self.instance.tag or "").strip()):
            return attrs
        if SPONSOR_TAG_MARKER.strip() not in tag:
            attrs["sponsor"] = None
            return attrs
        slug = tag.split(" ", 1)[0]
        sponsor = Sponsors.objects.filter(slug=slug).exclude(slug="").first()
        if sponsor is None:
            raise serializers.ValidationError({"tag": "Nepoznat sponzor za ovaj tag."})
        attrs["sponsor"], attrs["tag"] = sponsor, sponsor.guest_tag
        return attrs


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
        fields = ["id", "slug", "order", "visible", "name", "image", "biography"]

class PublicLineupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lineup
        fields = [
            'name',
            'image',
            'biography',
        ]

class SponsorsSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.SerializerMethodField()
    guestsAdded = serializers.IntegerField(read_only=True, default=0)
    guestsEntered = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Sponsors
        fields = ["id", "slug", "link", "order", "visible", "guestsEnabled",
                  "name", "url", "image", "email", "guestCap", "guestsAdded", "guestsEntered"]
        # Admin-only serializer; the token is generated once on create and never changes.
        # The slug is baked into guest tags (entry view, FirmeView search), so it is fixed at creation.
        read_only_fields = ["slug"]

    def get_link(self, obj):
        return sponsor_portal_link(obj)


class PublicSponsorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sponsors
        fields = ["name", "url", "image"]


class SponsorGuestSerializer(serializers.ModelSerializer):
    # Sponsors enter "Ime Prezime" as one field.
    name = serializers.CharField(max_length=100, trim_whitespace=True)

    class Meta:
        model = Guests
        fields = ["id", "name", "entered"]
        read_only_fields = ["entered"]


class SponsorPortalSerializer(serializers.ModelSerializer):
    guests = serializers.SerializerMethodField()

    class Meta:
        model = Sponsors
        fields = ["name", "image", "guestCap", "guests"]

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["open"], data["deadline"] = sponsor_input_state(obj)
        return data

    def get_guests(self, obj):
        return SponsorGuestSerializer(obj.guests.order_by("id"), many=True).data


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
        fields = ["name", "visible", "time"]


class TranslationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Translations
        fields = ["id", "key", "value"]

class GameLeaderboardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GameLeaderboard
        fields = ["id", "name", "email", "score"]


class DynamicSearchFilter(filters.SearchFilter):
    LOOKUP_PREFIXES = '^=@$'

    def get_search_fields(self, view, request):
        allowed = list(getattr(view, 'search_fields', None) or [])
        requested = request.GET.getlist('search_fields', [])
        if not requested:
            return allowed

        by_name = {f.lstrip(self.LOOKUP_PREFIXES): f for f in allowed}
        return [by_name[f] for f in requested if f in by_name]
    
NAME_RE = re.compile(r"[a-zA-ZčćđšžČĆĐŠŽ](?:[^\W\d_]|[ '’-])*")
NAME_ERROR = "Smije sadržavati samo slova"


class BrucosiFormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrucosiFormResponse
        fields = ['id', 'name', 'surname', 'jmbag', 'submitted_at', 'status', 'gdpr_accepted']
        read_only_fields = ['id', 'submitted_at', 'status']

    def validate_name(self, value):
        if not NAME_RE.fullmatch(value):
            raise serializers.ValidationError(NAME_ERROR)
        return value

    def validate_surname(self, value):
        return self.validate_name(value)

    def validate_jmbag(self, value):
        if not re.fullmatch(r"[0-9]{10}", value):
            raise serializers.ValidationError("JMBAG mora imati točno 10 znamenki.")
        return value

    def validate_gdpr_accepted(self, value):
        if value is not True:
            raise serializers.ValidationError("Prihvaćanje privole je obavezno.")
        return value
