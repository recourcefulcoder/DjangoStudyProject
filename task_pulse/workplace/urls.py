from django.urls import path
from django.views import generic

from workplace import views


app_name = "workplace"

urlpatterns = [
    path("tasks/", views.TaskList.as_view(), name="tasks"),
    path(
        "home/",
        views.HomeCompanyView.as_view(),
        name="home",
    ),
    path(
        "calendar/",
        generic.TemplateView.as_view(
            template_name="workplace/calendar.html",
        ),
        name="calendar",
    ),
    path("create_task/", views.TaskCreationForm.as_view(), name="create_task"),
    path(
        "company_invite/",
        views.AcceptCompanyInvite.as_view(),
        name="accept_company_invation",
    ),
]
