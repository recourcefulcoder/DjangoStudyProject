from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class CompanyUserStatistics(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        verbose_name=_("user"),
    )
    include_tasks = models.BooleanField(
        _("include tasks"),
        help_text=_("Does statistics include tasks?"),
    )
    statistics_file = models.FilePathField(
        _("user statistics file"),
        help_text=_("Path to file with user statistics"),
    )
    date_from = models.DateField(
        _("statistics from: (date)"),
        help_text=_("Start date user statistics"),
    )
    date_to = models.DateField(
        _("statistics to: (date)"),
        help_text=_("End date user statistics"),
    )
    created_at = models.DateTimeField(
        _("date of creation"),
        help_text=_("Date of creation user statistics report"),
        auto_now_add=True,
    )
