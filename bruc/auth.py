from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class RequireXHRHeader(BasePermission):
    """CSRF guard for cookie-authenticated endpoints. SameSite=Strict still sends the cookie from sibling
    *.kset.org origins, but a custom header forces a CORS preflight that origins outside CORS_ALLOWED_ORIGINS fail."""

    def has_permission(self, request, view):
        return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def set_refresh_cookie(response, token):
    """Store the refresh token where JS can't read it; only /api/auth/ ever receives it."""
    response.set_cookie(
        settings.AUTH_REFRESH_COOKIE,
        str(token),
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        path=settings.AUTH_REFRESH_COOKIE_PATH,
        secure=not settings.DEBUG,
        httponly=True,
        samesite="Strict",
    )


def blacklist_refresh_cookie(request):
    """Revoke the refresh token the browser sent, if it's still valid."""
    token = request.COOKIES.get(settings.AUTH_REFRESH_COOKIE)
    if token:
        try:
            RefreshToken(token).blacklist()
        except TokenError:
            pass


def clear_refresh_cookie(response):
    response.delete_cookie(
        settings.AUTH_REFRESH_COOKIE,
        path=settings.AUTH_REFRESH_COOKIE_PATH,
        samesite="Strict",
    )
