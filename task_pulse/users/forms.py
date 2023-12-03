from django.contrib.auth import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

from users import models


class SignupForm(forms.UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if models.User.objects.filter(email=email).exists():
            raise exceptions.ValidationError(
                _("User with this email is already exists"),
            )

        return email

    class Meta:
        model = models.User
        fields = [
            models.User.first_name.field.name,
            models.User.last_name.field.name,
            models.User.email.field.name,
        ]
