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
            companyuser__user=self.request.user,
        ).annotate(role=F("companyuser__role"))


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
            role=wp_models.ROLE_CHOICES[0],
        )
        company.save()
        company_user.save()
        return super().form_valid(form)


class InviteToCompanyView(mixins.LoginRequiredMixin, generic.FormView):
    template_name = "users/invite_to_company.html"
    form_class = forms.InviteToCompanyForm
    success_url = reverse_lazy("users:companies")

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Пользователь успешно приглашен в компанию!"),
        )
        # TODO проверка на приглашение себе
        company = wp_models.Company.objects.get(pk=self.kwargs["company_id"])
        if form.cleaned_data["expire_date"] is None:
            expire_date = None
        else:
            expire_date = datetime.date.today() + datetime.timedelta(
                days=int(form.cleaned_data["expire_date"]),
            )
        print(expire_date)
        invite = models.Invite.objects.create(
            invited_user_email=form.cleaned_data["invited_user_email"],
            expire_date=expire_date,
            company=company,
        )
        invite.clean()
        invite.save()
        return super().form_valid(form)


class UserInvitesListView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = "users/invites_list.html"
    context_object_name = "invites"

    def get_queryset(self):
        return models.Invite.objects.filter(
            invited_user_email=self.request.user.email,
        )
