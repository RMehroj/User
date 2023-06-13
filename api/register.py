from django.contrib.auth import get_user_model
from django.db import transaction

from . import models

User = get_user_model()


def authenticate(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def register_or_login_social_user(
    provider, social_media_id, email, name, last_name=None
):
    with transaction.atomic():
        user = User.objects.filter(email=email).first()
        if not user:
            company = models.Company.objects.create()
            user = User.objects.create_user(
                name=name,
                last_name=last_name or "",
                social_media_id=social_media_id,
                auth_provider=provider,
                email=email,
                password=User.objects.make_random_password(length=16),
                is_verified=True,

            )
        return {
            "name": user.name,
            "email": user.email,
            "tokens": user.tokens,
        }
