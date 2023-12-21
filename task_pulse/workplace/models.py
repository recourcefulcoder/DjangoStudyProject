from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


ROLE_CHOICES = [
    ("owner", _("Owner")),
    ("manager", _("Manager")),
    ("employee", _("Employee")),
]

TASK_STATUS_CHOICES = [
    ("in_processing", _("In Processing")),
    ("completed", _("Completed")),
    ("on_checking", _("On Checking")),
    ("rejected", _("Rejected")),
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
        related_name="company_users",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
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

    author = models.ForeignKey(
        CompanyUser,
        verbose_name=_("created by manager"),
        on_delete=models.DO_NOTHING,
        related_name="tasks_given",
    )

    status = models.CharField(
        _("task status"),
        help_text=_("Current task status"),
        choices=TASK_STATUS_CHOICES,
        max_length=20,
        default=TASK_STATUS_CHOICES[0][0],
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

    def clean(self):
        # checks whether "manager" field points on a manager or not
        if self.author.role != "manager" and self.author.role != "owner":
            raise ValidationError(
                "Invalid 'manager' choice - user must be manager!",
            )


class TaskStatusChangeLog(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        verbose_name=_("task object"),
        related_name="status_changes",
    )
    from_status = models.CharField(
        _("from status"),
        help_text=_("changed from: (task status)"),
        choices=TASK_STATUS_CHOICES,
        max_length=20,
    )
    to_status = models.CharField(
        _("to status"),
        help_text=_("changed to: (task status)"),
        choices=TASK_STATUS_CHOICES,
        max_length=20,
    )
    changed_at = models.DateTimeField(
        "change date",
        help_text=_("status change date"),
        auto_now_add=True,
    )
