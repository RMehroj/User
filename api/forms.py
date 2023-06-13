from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "is_active",
            "is_staff",
        )


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "is_active",
            "is_staff",
        )
