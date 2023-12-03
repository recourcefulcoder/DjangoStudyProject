from django.urls import reverse_lazy
from django.views import generic

from users import forms


class SignupView(generic.FormView):
    form_class = forms.SignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("homepage:homepage")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
