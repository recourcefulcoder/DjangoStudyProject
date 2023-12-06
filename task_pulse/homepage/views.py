from django.contrib.auth.forms import AuthenticationForm
from django.views import generic


class HomepageView(generic.TemplateView):
    template_name = "homepage/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = AuthenticationForm()
        context["signup_form"] = ""

        return context
