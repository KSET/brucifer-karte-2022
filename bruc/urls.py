from django.urls import path, include
from rest_framework import routers

from .views import (
    GameLeaderboardViewSet,
    TranslationsViewSet,
    VisibilityViewSet,
    CjenikViewSet,
    ContactViewSet,
    GuestsViewSet,
    MailerViewSet,
    TagsViewSet,
    UsersViewSet,
    LineupViewSet,
    PublicLineupViewSet,
    SponsorsViewSet,
    BrucosiFormResponseViewSet,
    GoogleAuthView,
    PublicSponsorsViewSet
)

router = routers.DefaultRouter()
router.register('guests', GuestsViewSet)
router.register('tags', TagsViewSet)
router.register('users', UsersViewSet)
router.register('lineup', LineupViewSet)                      
router.register('public/lineup', PublicLineupViewSet, basename='public-lineup')
router.register('public/sponsors', PublicSponsorsViewSet, basename='public-sponsors')
router.register('sponsors', SponsorsViewSet)
router.register('contact', ContactViewSet)
router.register('mailer', MailerViewSet)
router.register('cjenik', CjenikViewSet)
router.register('visibility', VisibilityViewSet)
router.register('translations', TranslationsViewSet)
router.register('gameLeaderboard', GameLeaderboardViewSet)
router.register('forms', BrucosiFormResponseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/google/', GoogleAuthView.as_view(), name="google-auth"),
]
