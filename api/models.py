import uuid as uuid_lib

from django.conf import settings

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from app.models import BaseModel

from . import managers

class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    class AUTH_PROVIDERS(models.TextChoices):
        GOOGLE = "google", "Google"
        FACEBOOK = "facebook", "Facebook"
        TWITTER = "twitter", "Twitter"
        EMAIL = "email", "Email"

    jwt_uuid = models.UUIDField(default=uuid_lib.uuid4, unique=True)
    social_media_id = models.CharField(max_length=50, blank=True)
    name = models.CharField(("name"), max_length=150, blank=True)
    last_name = models.CharField(("last name"), max_length=150, blank=True)
    email = models.EmailField(("email address"), unique=True)
    country = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_verified = models.BooleanField(
        default=False,
        help_text=("Designates whether this user's email address has been verified."),
    )
    is_available = models.BooleanField(
        default=True, help_text=("Designates whether the labeler is available.")
    )

    auth_provider = models.CharField(
        max_length=50,
        choices=AUTH_PROVIDERS.choices,
        )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = managers.UserManager()

    class Meta:
        verbose_name = ("user")
        verbose_name_plural = ("users")

    def __str__(self):
        return self.email
