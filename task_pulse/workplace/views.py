from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from workplace import forms, mixins, models


class HomeCompanyView(
    mixins.CompanyUserRequiredMixin,
    generic.TemplateView,
):
    template_name = "workplace/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = models.Task.objects.filter(
            responsible=context["company_user"],
        ).first()
        context["team"] = (
            models.CompanyUser.objects.select_related("user")
            .filter(company_id=self.kwargs.get("company_id"))
            .only(
                "user__email",
                "user__first_name",
                "user__last_name",
                "user__image",
                "role",
            )
        )
        if context["company_user"].role in ["owner", "manager"]:
            context["form"] = forms.TaskCreationForm(
                author=context["company_user"],
            )
        return context


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


class CompanyProfile(
    SuccessMessageMixin,
    mixins.CompanyOwnerRequiredMixin,
    generic.UpdateView,
):
    pk_url_kwarg = "company_id"
    model = models.Company
    form_class = forms.CompanyUpdateForm
    template_name = "workplace/settings/company.html"
    success_message = "Company info successfully changed!"

    def get_success_url(self):
        return reverse_lazy(
            "workplace:settings_company",
            kwargs={"company_id": self.kwargs.get("company_id")},
        )


class TeamView(
    mixins.CompanyManagerRequiredMixin,
    generic.ListView,
):
    model = models.CompanyUser
    context_object_name = "employees"
    template_name = "workplace/settings/team.html"

    def get_queryset(self):
        company_id = self.request.resolver_match.kwargs["company_id"]
        return (
            self.model.objects.select_related("user")
            .filter(company_id=company_id)
            .only(
                "user__first_name",
                "user__last_name",
                "user__email",
                "role",
                "user__image",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = forms.InviteMemberForm()
        return context


class ScheduleView(
    SuccessMessageMixin,
    mixins.CompanyOwnerRequiredMixin,
    generic.FormView,
):
    form_class = forms.CompanyScheduleForm
    template_name = "workplace/settings/schedule.html"
    success_message = "Schedule info successfully! changed"

    def form_valid(self, form):
        company_id = self.kwargs.get("company_id")
        models.Company.objects.filter(id=company_id).update(
            working_days=form.cleaned_data["week_choices"],
            start_time=form.cleaned_data["start_time"],
            end_time=form.cleaned_data["end_time"],
        )

        return redirect(
            "workplace:settings_schedule",
            company_id=self.kwargs.get("company_id"),
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "GET":
            company_id = self.kwargs.get("company_id")
            company = (
                models.Company.objects.filter(id=company_id)
                .values(
                    models.Company.start_time.field.name,
                    models.Company.end_time.field.name,
                    models.Company.working_days.field.name,
                )
                .first()
            )

            week_choices = {}
            working_days = company[models.Company.working_days.field.name]
            for num in range(len(working_days)):
                week_choices[f"week_choices_{num}"] = working_days[num] == "1"

            data = {
                "start_time": company[models.Company.start_time.field.name],
                "end_time": company[models.Company.end_time.field.name],
            }
            data.update(week_choices)

            kwargs.update(
                {
                    "data": data,
                },
            )
        return kwargs


class InviteMember(
    mixins.CompanyOwnerRequiredMixin,
    generic.FormView,
):
    http_method_names = ["post"]
    form_class = forms.InviteMemberForm

    def get_success_url(self):
        return reverse_lazy(
            "workplace:settings_team",
            kwargs={"company_id": self.kwargs.get("company_id")},
        )

    def form_valid(self, form):
        return super().form_valid(form)
