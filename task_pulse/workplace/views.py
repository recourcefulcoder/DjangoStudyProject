from core import mixins
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from workplace import forms, models


class HomeCompanyView(
    mixins.CompanyUserRequiredMixin,
    generic.DetailView,
):
    template_name = "workplace/home.html"
    model = models.Company
    context_object_name = "company"
    pk_url_kwarg = "company_id"


class TaskList(
    mixins.CompanyUserRequiredMixin,
    generic.edit.FormMixin,
    generic.ListView,
):
    template_name = "workplace/tasks.html"
    model = models.Task
    context_object_name = "tasks"
    form_class = forms.TaskCreationForm

    def get_queryset(self):
        return models.Task.objects.filter(
            responsible=self.get_company_user(
                self.request.resolver_match.kwargs["company_id"],
            ),
        )

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        company_id = self.request.resolver_match.kwargs["company_id"]
        company_user = self.get_company_user(company_id)
        task = models.Task(author=company_user)

        return form_class(
            **self.get_form_kwargs(),
            instance=task,
            author=company_user,
        )


class TaskCreationForm(
    mixins.CompanyManagerRequiredMixin,
    generic.FormView,
):
    form_class = forms.TaskCreationForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, _("Task created successfully!"))
            return HttpResponseRedirect(
                reverse_lazy(
                    "workplace:tasks",
                    args=(request.resolver_match.kwargs["company_id"],),
                ),
            )
        messages.error(request, _("Invalid data"))

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        company_id = self.request.resolver_match.kwargs["company_id"]
        company_user = self.get_company_user(company_id)
        task = models.Task(author=company_user)

        return form_class(
            **self.get_form_kwargs(),
            instance=task,
            author=company_user,
        )
