from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy
from django.views import generic

from users import forms
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
        )


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
