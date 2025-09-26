
from django.urls import path, include

from rest_framework import routers, views
from .views import GameLeaderboardViewSet, TranslationsViewSet, VisibilityViewSet, CjenikViewSet, ContactViewSet, GuestsViewSet, MailerViewSet, TagsViewSet, UsersViewSet, LineupViewSet, SponsorsViewSet, send_mail, BrucosiFormResponseViewSet

from rest_framework_simplejwt.views import TokenRefreshView
from .authviews import AuthExchange, me_view, logout_view

router = routers.DefaultRouter()
router.register('guests', GuestsViewSet)
router.register('tags', TagsViewSet)
router.register('users', UsersViewSet)
router.register('lineup', LineupViewSet)
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

    path('auth/exchange/', AuthExchange.as_view(), name='auth_exchange'),  # <-- here
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_view, name='logout'),
    path('me/', me_view, name='me'),
]
