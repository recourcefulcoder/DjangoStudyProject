from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views import generic

from users import models as us_models
from workplace import forms, mixins, models


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
    generic.ListView,
):
    template_name = "workplace/tasks.html"
    model = models.Task
    context_object_name = "tasks"

    def get_queryset(self):
        return models.Task.objects.filter(
            responsible=self.get_company_user(
                self.request.resolver_match.kwargs["company_id"],
            ),
        )


class TaskCreationForm(
    mixins.CompanyManagerRequiredMixin,
    generic.FormView,
):
    form_class = forms.TaskCreationForm
    template_name = "workplace/task_create_form.html"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            messages.success(request, _("Task created successfully!"))
        else:
            print(form.cleaned_data)
            messages.error(request, _("Invalid data"))

        return redirect(
            "workplace:create_task",
            company_id=self.request.resolver_match.kwargs["company_id"],
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


class AcceptCompanyInvite(
    auth_mixins.LoginRequiredMixin,
    generic.TemplateView,
):
    def get(self, request, *args, **kwargs):
        invite = us_models.Invite.objects.get(
            invited_user_email=request.user.email,
            company=models.Company.objects.get(id=kwargs["company_id"]),
        )
        models.CompanyUser.objects.get_or_create(
            user=request.user,
            company=models.Company.objects.get(id=kwargs["company_id"]),
            role=invite.assigned_role,
        )
        invite.delete()
        return redirect("workplace:home", company_id=kwargs["company_id"])
