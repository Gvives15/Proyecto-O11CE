"""
Middleware para autenticar mediante JWT en cookies HttpOnly
y refrescar el token de acceso de forma inteligente.

Flujo:
1. Si no hay cabecera Authorization, intenta sacar `access_token` de la cookie.
2. Valida el token; si faltan < 60 s para caducar genera uno nuevo (via refresh).
3. Inyecta `Authorization: Bearer <token>` en `request.META`.
4. Guarda el nuevo `access_token` (si hubo refresh) en la respuesta.

Ventajas:
- El frontend no maneja tokens manualmente.
- Solo refresca cuando es estrictamente necesario.
"""

import datetime as _dt

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"
# Segundos antes de expirar para forzar refresh (1 min)
REFRESH_WINDOW = 60


class JWTAuthenticationFromCookieMiddleware(MiddlewareMixin):
    """
    Middleware para convertir cookies JWT en cabeceras Authorization.
    """

    def process_request(self, request):
        # Si ya hay Authorization no hacemos nada
        if request.META.get("HTTP_AUTHORIZATION"):
            return

        access_token = request.COOKIES.get(ACCESS_COOKIE)
        refresh_token = request.COOKIES.get(REFRESH_COOKIE)
        if not access_token:
            return  # Usuario anónimo

        try:
            token = AccessToken(access_token)
            # Si el token vence en menos de REFRESH_WINDOW segundos, refrescar
            if (token["exp"] - int(_dt.datetime.utcnow().timestamp())) < REFRESH_WINDOW:
                raise TokenError("Token a punto de expirar")
            # Token válido ⇒ inyectar cabecera
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        except TokenError:
            # Intentar refrescar usando el refresh_token
            if not refresh_token:
                return  # No se puede refrescar
            try:
                new_access = RefreshToken(refresh_token).access_token
                # Guardar cabecera para la vista
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {str(new_access)}"
                # Marcar para que process_response guarde la cookie actualizada
                request._new_access_token = str(new_access)
            except TokenError:
                # Refresh inválido ⇒ ignorar (usuario quedará sin auth)
                pass

    def process_response(self, request, response):
        """
        Si en process_request se generó un nuevo access token, guardarlo.
        """
        new_token = getattr(request, "_new_access_token", None)
        if new_token:
            response.set_cookie(
                key=ACCESS_COOKIE,
                value=new_token,
                httponly=True,
                samesite="Lax",
                secure=not settings.DEBUG,  # Solo HTTPS en producción
                path="/",
                max_age=60 * 60,  # 1 h
            )
        return response
