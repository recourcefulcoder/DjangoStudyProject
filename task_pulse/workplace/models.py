import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


# order is important! "owner" must be first element in the list
ROLE_CHOICES = [
    ("owner", "Owner"),
    ("manager", "Manager"),
    ("employee", "Employee"),
]

TASK_STATES = [
    ("given", "Given"),
    ("active", "Active"),
    ("postponed", "Postponed"),
    ("review", "On review"),
    ("rejected", "Rejected"),
    ("completed", "Completed"),
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
    start_time = models.TimeField(
        help_text=_("time of beginning of working day"),
        default=datetime.time(hour=9),
    )
    end_time = models.TimeField(
        help_text=_("time of ending of working day"),
        default=datetime.time(hour=18),
    )
    # string of 7 chars "1" or "0", implementing , whether
    # corresponding day considered as working or not, respectively
    working_days = models.CharField(
        max_length=7,
        default="1111100",
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

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


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

    author = models.ForeignKey(
        CompanyUser,
        verbose_name=_("created by manager"),
        on_delete=models.DO_NOTHING,
        related_name="tasks_given",
    )

    state = models.CharField(
        _("state"),
        choices=TASK_STATES,
        max_length=20,
        help_text=_("Task current state"),
        default="given",
    )

    def clean(self):
        # checks whether "manager" field points on a manager or not
        if self.author.role != "manager" and self.author.role != "owner":
            raise ValidationError(
                "Invalid 'manager' choice - user must be manager!",
            )
