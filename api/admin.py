from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from . import models
from .forms import UserChangeForm, UserCreationForm

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    readonly_fields = [
        "created",
        "updated",
        "last_login",
    ]
    list_display = [
        "pk",
        "email",
        "name",
        "is_staff",
        "is_active",
        "is_verified",
    ]
    list_filter = [
        "is_staff",
        "is_active",
        "is_verified",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": ("name",),
            },
        ),
        (
            None,
            {
                "fields": (
                    "email",
                    "auth_provider",
                    "password",
                ),
            },
        ),
        (
            None,
            {
                "fields": (
                    "created",
                    "updated",
                    "last_login",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "user_permissions",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_verified",
                    "is_available",
                )
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    "email",
                    "auth_provider",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                    "is_verified",
                    "is_available",
                ),
            },
        ),
    ]
    search_fields = ("email",)
    ordering = ("-created",)
