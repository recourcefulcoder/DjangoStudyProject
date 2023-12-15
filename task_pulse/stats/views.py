from django.http import HttpResponseRedirect
from django.views import generic

from core import mixins
from stats import forms


class CreateStatisticsReport(
    mixins.CompanyManagerRequiredMixin,
    generic.FormView,
):
    template_name = "statistics/statistics_report_create.html"
    form_class = forms.CreateStatisticsReportForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            statistics_report = form.save(commit=False)
            if form.cleaned_data["include_tasks"]:
                pass
