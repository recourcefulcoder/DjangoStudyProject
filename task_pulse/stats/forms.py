from django import forms

from stats import models
from workplace import models as wp_models


class CreateUserStatisticsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = wp_models.CompanyUser.objects.filter(
            role="employee",
        )

    class Meta:
        model = models.CompanyUserStatistics
        exclude = [
            models.CompanyUserStatistics.created_at.field.name,
            models.CompanyUserStatistics.statistics_file.field.name,
        ]


class CreateCompanyStatisticsForm(forms.ModelForm):
    class Meta:
        model = models.CompanyStatistics
        exclude = [
            models.CompanyStatistics.company.field.name,
            models.CompanyStatistics.created_at.field.name,
            models.CompanyStatistics.statistics_file.field.name,
        ]
