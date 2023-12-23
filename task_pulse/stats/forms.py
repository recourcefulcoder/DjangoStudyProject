from django import forms

from stats import models
from workplace import models as wp_models


class CreateUserStatisticsForm(forms.ModelForm):
    def __init__(self, initial, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.name != "include_tasks":
                field.field.widget.attrs["class"] = "form-control"
            else:
                field.field.widget.attrs["class"] = "form-check-input"

        self.fields["user"].queryset = wp_models.CompanyUser.objects.filter(
            role="employee",
            company__id=initial["company_id"],
        )

    class Meta:
        model = models.CompanyUserStatistics
        exclude = [
            models.CompanyUserStatistics.created_at.field.name,
            models.CompanyUserStatistics.statistics_file.field.name,
        ]


class CreateCompanyStatisticsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.name != "include_tasks" and field.name != "include_users":
                field.field.widget.attrs["class"] = "form-control"
            else:
                field.field.widget.attrs["class"] = "form-check-input"

    class Meta:
        model = models.CompanyStatistics
        exclude = [
            models.CompanyStatistics.company.field.name,
            models.CompanyStatistics.created_at.field.name,
            models.CompanyStatistics.statistics_file.field.name,
        ]
