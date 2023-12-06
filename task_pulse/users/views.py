from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy
from django.views import generic
from workplace import models as wp_models

from users import forms


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
    queryset = wp_models.Company.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies"] = wp_models.Company.objects.filter(
            companyuser__user__pk=self.kwargs["pk"],
        )
        return context


class UserSettingsView(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = "users/profile_settings.html"
    model = get_user_model()
    context_object_name = "current_user"
