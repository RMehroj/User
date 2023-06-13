import os

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.utils import timezone
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from app.serializers import DynamicFieldsModelSerializer

from app.tasks import send_html_email

from . import google, models


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, data):
        tokens = super().validate(data)
        data = UserReadSerializer(self.user, context=self.context).data
        data.update({"tokens": tokens})
        return data
    
class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(write_only=True, allow_blank=False)

    @staticmethod
    def map_user_data(data: dict):
        user_data = dict(
            social_media_id=data["sub"],
            email=data["email"],
            name=data["given_name"],
            last_name=data["family_name"],
            provider="google",
        )
        return user_data

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data["sub"]
        except Exception:
            raise serializers.ValidationError(
                detail={"error": "The token is invalid or expired"}
            )
        if user_data["aud"] != os.environ.get("GOOGLE_CLIENT_ID"):
            raise AuthenticationFailed(
                detail={"error": "Your Google client id is invalid."}
            )
        return self.map_user_data(user_data)

class UserReadSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "name",
            "last_name",
            "email",
            "is_verified",
        ]

class UserWriteSerializer(DynamicFieldsModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = [
            "pk",
            "name",
            "last_name",
            "email",
            "password",
            "is_verified",
        ]
        read_only_fields = [
            "is_verified",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            validated_data.setdefault("auth_provider", "email")
            user = get_user_model().objects.create_user(
                **validated_data
            )
            payload = {
                "user_id": user.pk.__str__(),
                "exp": timezone.localtime(timezone.now()) + timezone.timedelta(hours=1),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            url = f"http://api.gnexus.uz/verify?auth={token}"
            html_message = render_to_string(
                "user/email_confirmation.html",
                context={"url": url},
            )
            send_html_email.delay("Verify your email", html_message, [user.email])
            return user
        
class EmailVerificationSerializer(serializers.Serializer):
    auth_token = serializers.CharField(write_only=True, min_length=50)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                detail={"error": "Passwords do not match"}
            )
        if not check_password(
            data["old_password"], self.context["request"].user.password
        ):
            raise serializers.ValidationError(
                detail={"error": "Old password is invalid"}
            )
        return data


class PasswordResetSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True, allow_blank=False, min_length=8)
    password2 = serializers.CharField(write_only=True, allow_blank=False, min_length=8)
    auth_token = serializers.CharField(
        write_only=True, allow_blank=False, min_length=50
    )

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                detail={"error": "The passwords do not match."}
            )
        return data