from django import forms as pure_forms
from django.contrib.auth import forms
from django.core import exceptions
from django.utils.translation import gettext_lazy as _

from users import models
from workplace import models as wp_models


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


class ProfileForm(forms.UserChangeForm):
    image = pure_forms.ImageField(widget=pure_forms.FileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = models.User
        fields = [
            models.User.first_name.field.name,
            models.User.last_name.field.name,
            models.User.email.field.name,
            models.User.image.field.name,
        ]


class CreateCompanyForm(pure_forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = wp_models.Company
        fields = [
            wp_models.Company.name.field.name,
            wp_models.Company.description.field.name,
        ]
