from django import forms

from stats import models


class CreateStatisticsReportForm(forms.ModelForm):
    class Meta:
        model = models.CompanyUserStatistics
        exclude = [
            models.CompanyUserStatistics.created_at.field.name,
            models.CompanyUserStatistics.statistics_file.field.name,
        ]
