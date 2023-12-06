from django.views import generic
from workplace import mixins, models


class HomeCompanyView(
    mixins.CompanyUserRequiredMixin,
    generic.DetailView,
):
    template_name = "workplace/tasks.html"
    model = models.Company
    context_object_name = "company"
    pk_url_kwarg = "company_id"
