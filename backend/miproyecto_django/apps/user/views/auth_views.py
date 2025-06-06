"""
Vistas de autenticación: registro, login y logout.
"""

from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.serializers import RegisterSerializer, UserSerializer

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"


class RegisterView(generics.CreateAPIView):
    """
    Registro de usuarios (abierto).
    """
    serializer_class = RegisterSerializer
    permission_classes = []  # Público


class LoginView(APIView):
    """
    Autenticación: devuelve tokens JWT en cookies HttpOnly.
    """

    permission_classes = []  # Público

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"detail": "Credenciales inválidas."},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Generar pares de tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        resp = Response(UserSerializer(user).data)
        # Guardar cookies seguras
        resp.set_cookie(
            ACCESS_COOKIE, str(access), httponly=True, samesite="Lax",
            secure=not settings.DEBUG, path="/"
        )
        resp.set_cookie(
            REFRESH_COOKIE, str(refresh), httponly=True, samesite="Lax",
            secure=not settings.DEBUG, path="/"
        )
        return resp


class LogoutView(APIView):
    """
    Cierra sesión: borra cookies JWT.
    """

    def post(self, request):
        resp = Response({"detail": "Sesión finalizada."},
                        status=status.HTTP_200_OK)
        resp.delete_cookie(ACCESS_COOKIE, path="/")
        resp.delete_cookie(REFRESH_COOKIE, path="/")
        return resp
