import json
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Users 

User = get_user_model()

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def _set_refresh_cookie(resp, refresh_token: str):
    resp.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,  
        secure=not settings.DEBUG,
        samesite="Lax",
        path="/",
        max_age=30 * 24 * 3600,
    )


@method_decorator(csrf_exempt, name="dispatch")
class AuthExchange(APIView):
    """
    POST /auth/exchange
    Body: { code, code_verifier, redirect_uri, provider? }
    - Exchanges an OAuth authorization code (PKCE) with Google
    - Fetches userinfo, upserts local Django user + Users row
    - Issues JWT (access in body) and sets refresh cookie
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            body = json.loads(request.body.decode("utf-8"))
            code = body["code"]
            code_verifier = body["code_verifier"]
            redirect_uri = body["redirect_uri"]
            provider = (body.get("provider") or "google").lower()
        except Exception:
            return HttpResponseBadRequest("Invalid payload")

        if provider != "google":
            return HttpResponseBadRequest("Unsupported provider")

        # Exchange code for tokens
        data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
        }
        if getattr(settings, "GOOGLE_CLIENT_SECRET", None):
            data["client_secret"] = settings.GOOGLE_CLIENT_SECRET

        tok = requests.post(GOOGLE_TOKEN_URL, data=data, timeout=10)
        if tok.status_code != 200:
            return HttpResponseBadRequest("Token exchange failed")

        tokens = tok.json()
        provider_access = tokens.get("access_token")
        if not provider_access:
            return HttpResponseBadRequest("No access_token from provider")

        # Fetch userinfo from Google
        ui = requests.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {provider_access}"},
            timeout=10,
        )
        if ui.status_code != 200:
            return HttpResponseBadRequest("Failed to fetch userinfo")

        info = ui.json()
        email = info.get("email")
        name = info.get("name") or ""
        if not email:
            return HttpResponseBadRequest("No email from provider")

        # Upsert Django auth user (for JWT)
        user, _ = User.objects.get_or_create(
            username=email, defaults={"email": email, "first_name": name}
        )
        if name and user.first_name != name:
            user.first_name = name
            user.save(update_fields=["first_name"])

        # Upsert into your Users table
        u_row, created = Users.objects.get_or_create(
            email=email,
            defaults={"name": name, "privilege": 0},
        )
        if name and u_row.name != name:
            u_row.name = name
            u_row.save(update_fields=["name"])

        # Issue JWTs
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        resp = JsonResponse({"access": access})
        _set_refresh_cookie(resp, str(refresh))
        return resp


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Return currently logged-in user info + privilege from Users table"""
    auth_user = request.user
    u_row = Users.objects.filter(email=auth_user.email).first()

    return Response({
        "id": u_row.id if u_row else None,
        "email": auth_user.email,
        "name": auth_user.first_name or auth_user.get_username(),
        "privilege": u_row.privilege if u_row else 0,
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    """Clear refresh cookie (logout)"""
    resp = Response({"ok": True})
    resp.delete_cookie("refresh_token", path="/")
    return resp
