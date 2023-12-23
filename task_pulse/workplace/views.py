import http
import json

from core import mixins
from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from django.views.decorators.http import require_POST

from users import forms as us_forms
from users import models as us_models
from users import views
from workplace import forms, models


class HomeCompanyView(
    mixins.CompanyUserRequiredMixin,
    generic.edit.FormMixin,
    generic.TemplateView,
):
    template_name = "workplace/home.html"
    form_class = forms.TaskCreationForm
    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = models.Task.objects.filter(
            responsible=context["company_user"],
            status="active",
        ).first()

        if context["company_user"].role in ["owner", "manager"]:
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
        return context

    def post(self, *args, **kwargs):
        self.get_form().save()
        messages.success(self.request, "Task successfully added!")
        return redirect(
            "workplace:home",
            **kwargs,
        )

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        company_id = self.kwargs.get("company_id")
        company_user = self.get_company_user(company_id)
        task = models.Task(author=company_user)

        return form_class(
            **self.get_form_kwargs(),
            instance=task,
            author=company_user,
        )


class TaskList(
    mixins.CompanyUserRequiredMixin,
    generic.edit.FormMixin,
    generic.ListView,
):
    template_name = "workplace/tasks.html"
    context_object_name = "tasks"
    form_class = forms.TaskCreationForm

    def get_queryset(self):
        queryset = (
            models.Task.objects.select_related(
                "author",
                "author__user",
                "review_responsible__user",
                "review",
            )
            .filter(
                responsible=self.get_company_user(
                    self.request.resolver_match.kwargs.get("company_id"),
                ),
            )
            .only(
                "title",
                "description",
                "deadline",
                "status",
                "author__user__first_name",
                "author__user__last_name",
                "author__user__email",
                "review_responsible__user__first_name",
                "review_responsible__user__last_name",
                "review_responsible__user__email",
                "review",
            )
        )
        # for each in queryset:
        #     print(each.title)
        #     if each.title == "review":
        #         print("HErE")
        #         print(each.review)
        #         print(each.review.message)
        #     if hasattr(each, "review"):
        #         print(each.review, each.review.message)
        return queryset

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        company_id = self.kwargs.get("company_id")
        company_user = self.get_company_user(company_id)
        task = models.Task(author=company_user)

        return form_class(
            **self.get_form_kwargs(),
            instance=task,
            author=company_user,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_choices"] = [
            ("given", "Given"),
            ("postponed", "Postponed"),
            ("review", "On review"),
            ("rejected", "Rejected"),
        ]
        active_tasks = self.object_list.filter(status="active")
        if active_tasks.exists():
            context["active_task"] = active_tasks.first()
        return context


class ReviewList(
    mixins.CompanyUserRequiredMixin,
    generic.edit.FormMixin,
    generic.ListView,
):
    template_name = "workplace/review.html"
    context_object_name = "tasks"
    form_class = forms.ReviewRejectForm

    def get_queryset(self):
        return (
            models.Task.objects.select_related("author", "author__user")
            .filter(
                review_responsible=self.get_company_user(
                    self.request.resolver_match.kwargs["company_id"],
                ),
                status="review",
            )
            .only(
                "title",
                "description",
                "deadline",
                "status",
                "author__user__first_name",
                "author__user__last_name",
                "author__user__email",
            )
        )

    def post(self, *args, **kwargs):
        if self.request.POST:
            data = self.request.POST
            data["approved"] = data["approved"][0]
            if data["approved"] == "false":
                data["approved"] = False
        else:
            data = json.loads(self.request.body.decode("utf8"))

        task = models.Task.objects.get(pk=int(data["task_id"]))
        print(data["approved"], type(data["approved"]))
        if data["approved"]:
            task.status = "completed"
        else:
            task.status = "rejected"
            # hardcode - depends on manual form in template
            models.Review.objects.create(task=task, message=data["message"])
        task.save()

        messages.success(self.request, "Review successfully sent")
        return HttpResponse("completed", http.HTTPStatus.OK)


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
        context["form"] = us_forms.InviteToCompanyForm()
        return context


class ScheduleView(
    SuccessMessageMixin,
    mixins.CompanyOwnerRequiredMixin,
    generic.FormView,
):
    form_class = forms.CompanyScheduleForm
    template_name = "workplace/settings/schedule.html"
    success_message = "Schedule info successfully changed!"

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
    views.InviteToCompanyInterface,
):
    http_method_names = ["post"]

    def get_success_url(self):
        return reverse_lazy(
            "workplace:settings_team",
            kwargs={"company_id": self.kwargs.get("company_id")},
        )

    def form_invalid(self, form):
        messages.error(
            self.request,
            _("Invite was not sent"),
        )
        return redirect(self.get_success_url())


@require_POST
@login_required
def change_task_status(request, company_id):
    company_user = models.CompanyUser.objects.get(
        user=request.user,
        company_id=request.resolver_match.kwargs.get("company_id"),
    )
    if company_user.company.id != company_id:
        return HttpResponse(
            _("access forbidden: you are not user of this company!"),
            http.HTTPStatus.FORBIDDEN,
        )

    data = json.loads(request.body.decode("utf8"))

    if data["status"] == "active":
        tasks = models.Task.objects.filter(status="active")
        if tasks.exists():
            for task in tasks:
                task.status = "postponed"
                task.save()

    task = models.Task.objects.get(pk=int(data["pk"]))

    if task.status == "review":
        if company_user != task.review_responsible:
            return HttpResponse(
                _("access forbidden: you are not reviewer of thid task!"),
                http.HTTPStatus.FORBIDDEN,
            )

    task.status = data["status"]
    task.save()

    return HttpResponse("DONE!")


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
