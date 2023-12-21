from django.db import models
from django.utils.translation import gettext_lazy as _

from workplace import models as wp_models


class CompanyUserStatistics(models.Model):
    user = models.ForeignKey(
        wp_models.CompanyUser,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    include_tasks = models.BooleanField(
        _("include tasks"),
        help_text=_("Does report include tasks?"),
    )
    statistics_file = models.FileField(
        _("user statistics file"),
        help_text=_("Path to file with user statistics"),
        upload_to="statistics/users",
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


class CompanyStatistics(models.Model):
    company = models.ForeignKey(
        wp_models.Company,
        on_delete=models.CASCADE,
        verbose_name=_("company"),
    )
    include_users = models.BooleanField(
        _("include users"),
        help_text=_("Does report include user statistics in this company?"),
    )
    include_tasks = models.BooleanField(
        _("include tasks"),
        help_text=_("Does report include user tasks?"),
    )
    statistics_file = models.FileField(
        _("company statistics file"),
        help_text=_("Path to file with company statistics"),
        upload_to="statistics/company",
    )
    date_from = models.DateField(
        _("statistics from: (date)"),
        help_text=_("Start date company statistics"),
    )
    date_to = models.DateField(
        _("statistics to: (date)"),
        help_text=_("End date company statistics"),
    )
    created_at = models.DateTimeField(
        _("date of creation"),
        help_text=_("Date of creation company statistics report"),
        auto_now_add=True,
    )
