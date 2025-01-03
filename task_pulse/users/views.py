import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model, mixins
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from users import forms
from users import models
from workplace import models as wp_models


class SignupView(generic.FormView):
    form_class = forms.SignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("homepage:homepage")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserCompaniesView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = "users/profile_companies.html"
    context_object_name = "companies"

    def get_queryset(self):
        return wp_models.Company.objects.filter(
            users__user=self.request.user,
        ).annotate(role=F("users__role"))


class UserChangeView(mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = "users/profile_settings.html"
    form_class = forms.ProfileForm
    model = get_user_model()
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user


class CreateCompanyView(mixins.LoginRequiredMixin, generic.FormView):
    template_name = "users/create_company.html"
    model = wp_models.Company
    form_class = forms.CreateCompanyForm
    success_url = reverse_lazy("users:companies")

    def form_valid(self, form):
        company = wp_models.Company.objects.create(
            **form.cleaned_data,
        )
        company_user = wp_models.CompanyUser.objects.create(
            user=self.request.user,
            company=company,
            role=wp_models.ROLE_CHOICES[0][0],
        )
        company.save()
        company_user.save()
        return super().form_valid(form)


class InviteToCompanyInterface(mixins.LoginRequiredMixin, generic.FormView):
    form_class = forms.InviteToCompanyForm

    def form_valid(self, form):
        invited_email = form.cleaned_data["invited_user_email"]

        if self.request.user.email == invited_email:
            messages.error(
                self.request,
                _("Forbidden to add yourself!"),
            )
            return super().form_valid(form)

        if models.Invite.objects.filter(
            invited_user_email=invited_email,
        ).exists():
            messages.error(
                self.request,
                _("Already invited user provided!"),
            )
            return super().form_valid(form)

        company = wp_models.Company.objects.get(
            pk=self.kwargs.get("company_id"),
        )
        pure_expire_date = int(form.cleaned_data["expire_date"])
        if pure_expire_date > 0:
            expire_date = datetime.date.today() + datetime.timedelta(
                days=int(pure_expire_date),
            )
        else:
            expire_date = None

        invite = models.Invite.objects.create(
            invited_user_email=form.cleaned_data["invited_user_email"],
            expire_date=expire_date,
            assigned_role=form.cleaned_data["assigned_role"],
            company=company,
        )
        invite.clean()
        invite.save()

        messages.success(
            self.request,
            _("User successfully invited to team!"),
        )

        invite.send_email()
        return super().form_valid(form)


class InviteToCompanyView(InviteToCompanyInterface):
    template_name = "users/invite_to_company.html"
    success_url = reverse_lazy("users:companies")


class UserInvitesListView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = "users/invites_list.html"
    context_object_name = "invites"

    def get_queryset(self):
        return models.Invite.objects.filter(
            invited_user_email=self.request.user.email,
        )
