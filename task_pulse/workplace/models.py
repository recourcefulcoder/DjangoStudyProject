from django.core.exceptions import ValidationError
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
        _("name"),
        max_length=150,
        help_text=_("Name for company"),
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


class Task(models.Model):
    title = models.CharField(
        _("name"),
        max_length=300,
        help_text=_("Task name"),
    )

    description = models.TextField(
        _("task description"),
        blank=True,
        help_text=_("concrete task description"),
    )

    deadline = models.DateTimeField(
        help_text=_("task deadline"),
    )

    responsible = models.ForeignKey(
        CompanyUser,
        verbose_name=_("responsible"),
        on_delete=models.DO_NOTHING,
        related_name="tasks",
    )

    manager = models.ForeignKey(
        CompanyUser,
        verbose_name=_("created by manager"),
        on_delete=models.DO_NOTHING,
        related_name="tasks_given",
    )

    def clean(self):
        # checks whether "manager" field points on a manager or not
        if self.manager.role != "manager":
            raise ValidationError("Invalid 'manager' choice - user must be manager!")
