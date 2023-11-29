from django.urls import path
from django.views import generic

app_name = "homepage"

urlpatterns = [
    path(
        "",
        generic.TemplateView.as_view(
            template_name="homepage/homepage.html",
        ),
    ),
]
