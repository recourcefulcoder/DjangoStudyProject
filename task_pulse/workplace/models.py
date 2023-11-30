from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


ROLE_CHOICES = [
    ("owner", "Owner"),
    ("manager", "Manager"),
    ("employee", "Employee"),
]


class Company(models.Model):
    name = models.CharField(
        _("name"), max_length=150, help_text=_("Name for company"),
    )
    description = models.TextField(
        _("description"),
        help_text=_("Description for company"),
        blank=True,
    )


class CompanyUser(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    role = models.CharField(
        _("role"),
        choices=ROLE_CHOICES,
        max_length=20,
        help_text=_("Role for company user"),
    )
    score = models.PositiveIntegerField(
        _("score"),
        help_text=_("User score count"),
        default=0,
    )
