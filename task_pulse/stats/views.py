import json

from core import mixins
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from stats import forms, models, utils
from workplace import models as wp_models


class CreateUserStatistics(
    mixins.CompanyManagerRequiredMixin,
    generic.FormView,
):
    template_name = "statistics/statistics_report_create.html"
    form_class = forms.CreateUserStatisticsForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            statistics_report = form.save(commit=False)
            statistics_data = utils.create_user_statistics(**form.cleaned_data)
            json_data = json.dumps(statistics_data, ensure_ascii=False).encode(
                "utf-8",
            )
            statistics_report.statistics_file.save(
                f"""{form.cleaned_data["user"].id}_"""
                f"""{timezone.now().strftime("%Y%m%d%H%M%S")}.json""",
                ContentFile(json_data),
            )
            statistics_report.save()

        return HttpResponseRedirect(
            reverse_lazy(
                "workplace:statistics",
                args=(request.resolver_match.kwargs["company_id"],),
            ),
        )


class CreateCompanyStatistics(
    mixins.CompanyManagerRequiredMixin,
    generic.FormView,
):
    template_name = "statistics/statistics_report_create.html"
    form_class = forms.CreateCompanyStatisticsForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            company = wp_models.Company.objects.get(
                id=self.request.resolver_match.kwargs["company_id"],
            )
            statistics_report = form.save(commit=False)
            statistics_data = utils.create_company_statistics(
                company=company,
                **form.cleaned_data,
            )
            json_data = json.dumps(statistics_data, ensure_ascii=False).encode(
                "utf-8",
            )
            statistics_report.company = company
            statistics_report.statistics_file.save(
                f"""{self.request.resolver_match.kwargs["company_id"]}_"""
                f"""{timezone.now().strftime("%Y%m%d%H%M%S")}.json""",
                ContentFile(json_data),
            )
            statistics_report.save()

        return HttpResponseRedirect(
            reverse_lazy(
                "workplace:statistics",
                args=(request.resolver_match.kwargs["company_id"],),
            ),
        )


class StatisticsListView(
    mixins.CompanyManagerRequiredMixin,
    generic.TemplateView,
):
    model = models.CompanyUserStatistics
    template_name = "statistics/statistics_list.html"
    form_class = forms.CreateUserStatisticsForm

    def get_context_data(self, **kwargs):
        kwargs["user_form"] = forms.CreateUserStatisticsForm
        kwargs["company_form"] = forms.CreateCompanyStatisticsForm

        kwargs[
            "users_stats_list"
        ] = models.CompanyUserStatistics.objects.filter(
            user__company__id=self.request.resolver_match.kwargs["company_id"],
            user__role="employee",
        )
        kwargs["company_stats_list"] = models.CompanyStatistics.objects.filter(
            company__id=self.request.resolver_match.kwargs["company_id"],
        )

        return super().get_context_data(**kwargs)
