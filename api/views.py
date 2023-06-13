import uuid as uuid_lib

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .register import register_or_login_social_user

from api.serializers import LoginSerializer, UserWriteSerializer, UserReadSerializer, GoogleSocialAuthSerializer, EmailVerificationSerializer

class LoginView(TokenObtainPairView):
    authentication_classes = []
    serializer_class = LoginSerializer

class UserVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserReadSerializer

    def get(self, request):
        data = self.get_serializer(request.user).data
        return Response(data, status=200)

class GoogleSocialAuthView(generics.GenericAPIView):
    authentication_classes = []
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data["auth_token"]
        data = register_or_login_social_user(**user_data)
        return Response(data, status=200)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserWriteSerializer
    authentication_classes = []
    model = get_user_model()


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    authentication_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["auth_token"]
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = get_user_model().objects.filter(pk=data["user_id"]).first()
            if not user:
                return Response(
                    {"error": "User not found."},
                    status=400,
                )
            if user.is_verified:
                return Response(
                    {"error": "Email already verified"},
                    status=200,
                )
            user.is_verified = True
            user.save(update_fields=["is_verified"])
            return Response(
                {"detail": "Email activated successfully"},
                status=200,
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation link expired"},
                status=400,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"},
                status=400,
            )