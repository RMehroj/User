from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import LoginView, UserVerifyView, GoogleSocialAuthView, RegisterView, VerifyEmailView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "verify/",
        UserVerifyView.as_view(),
        name="user_verify",
    ),
    path(
        "google/",
        GoogleSocialAuthView.as_view(),
        name="google_social_auth",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "verify-email/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),

]