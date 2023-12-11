from django.views import generic
from workplace import mixins, models, forms


class HomeCompanyView(
    mixins.CompanyUserRequiredMixin,
    generic.DetailView,
):
    template_name = "workplace/tasks.html"
    model = models.Company
    context_object_name = "company"
    pk_url_kwarg = "company_id"
    
    object = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["company_id"] = kwargs["company_id"]
        return self.render_to_response(context)


class TaskCreationForm(
    mixins.CompanyManagerRequiredMixin,
    generic.CreateView,
):
    form_class = forms.TaskCreationForm
    template_name = "workplace/task_create_form.html"
    object = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["company_id"] = kwargs["company_id"]
        return self.render_to_response(context)
