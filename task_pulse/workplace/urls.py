from django.urls import path
from django.views import generic
from workplace import views


app_name = "workplace"

urlpatterns = [
    path("tasks/", views.HomeCompanyView.as_view(), name="tasks"),
    path(
        "home/",
        generic.TemplateView.as_view(
            template_name="workplace/tasks.html",
        ),
        name="home",
    ),
    path(
        "calendar/",
        generic.TemplateView.as_view(
            template_name="workplace/tasks.html",
        ),
        name="calendar",
    ),
]
