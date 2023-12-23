import datetime

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# order is important! "owner" must be first element in the list
ROLE_CHOICES = [
    ("owner", _("Owner")),
    ("manager", _("Manager")),
    ("employee", _("Employee")),
]

TASK_STATUS_CHOICES = [
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

    def __str__(self):
        return self.name


class CompanyUser(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        verbose_name=_("user"),
        related_name="company_users",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.DO_NOTHING,
        verbose_name=_("company"),
        related_name="users",
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
        help_text=_("Concrete task description"),
    )

    deadline = models.DateTimeField(
        help_text=_("Task deadline"),
    )

    responsible = models.ForeignKey(
        CompanyUser,
        verbose_name=_("responsible"),
        on_delete=models.DO_NOTHING,
        related_name="tasks",
    )

    review_responsible = models.ForeignKey(
        CompanyUser,
        verbose_name=_("responsible for review"),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="review_tasks",
        help_text=_("leave blank if no review specified"),
    )

    author = models.ForeignKey(
        CompanyUser,
        verbose_name=_("created by manager"),
        on_delete=models.DO_NOTHING,
        related_name="tasks_given",
    )

    status = models.CharField(
        _("status"),
        choices=TASK_STATUS_CHOICES,
        max_length=20,
        help_text=_("Task current status"),
        default="given",
    )

    created_at = models.DateTimeField(
        _("create date"),
        help_text=_("Date of creation task"),
        auto_now_add=True,
    )

    completed_at = models.DateTimeField(
        _("complete date"),
        help_text=_("Date of task complition"),
        null=True,
        blank=True,
    )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if self.status == "completed" and self.completed_at is None:
            self.completed_at = timezone.now()

        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ["deadline"]

    def clean(self):
        # checks whether "manager" field points on a manager or not
        if self.author.role != "manager" and self.author.role != "owner":
            raise ValidationError(
                _("Invalid 'manager' choice - user must be manager!"),
            )
        if self.responsible == self.review_responsible:
            raise ValidationError(
                _("Reviewer and responsible can't be the same person!"),
            )
        if self.deadline < timezone.now():
            raise ValidationError(
                _("Invalid deadline value!"),
            )


class Review(models.Model):
    task = models.OneToOneField(
        Task,
        verbose_name=_("task"),
        on_delete=models.CASCADE,
        related_query_name="review",
    )
    message = models.TextField(
        verbose_name=_("review_message"),
    )
