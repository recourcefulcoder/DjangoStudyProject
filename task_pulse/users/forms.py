from django import forms as pure_forms
from django.conf import settings
from django.contrib.auth import forms
from django.core import exceptions, mail
from django.utils.translation import gettext_lazy as _

from users import models
from workplace import models as wp_models


INVITE_EXPIRE_DATE_CHOISES = (
    (1, _("day")),
    (3, _("tree days")),
    (7, _("week")),
    (14, _("two weeks")),
    (30, _("month")),
    (None, _("never")),
)


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


class InviteToCompanyForm(pure_forms.Form):
    invited_user_email = pure_forms.EmailField(
        required=True,
        label=_("email of invited emploee"),
    )

    expire_date = pure_forms.ChoiceField(
        choices=INVITE_EXPIRE_DATE_CHOISES,
        required=True,
        label=_("invite expire date"),
    )

    assigned_role = pure_forms.ChoiceField(
        choices=models.INVITE_ROLE_CHOISES,
        required=True,
        label=_("the role to be assigned"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    def send_email(self, text):
        mail.send_mail(
            "You are invited to company!",
            text,
            settings.MAIL,
            [self.cleaned_data["invited_user_email"]],
        )
