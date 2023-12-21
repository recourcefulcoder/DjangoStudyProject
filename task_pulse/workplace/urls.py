from django.urls import path

from workplace import views


app_name = "workplace"

urlpatterns = [
    path("tasks/", views.TaskList.as_view(), name="tasks"),
    path("reviews/", views.ReviewList.as_view(), name="review"),
    path(
        "home/",
        views.HomeCompanyView.as_view(),
        name="home",
    ),
    path(
        "calendar/",
        views.HomeCompanyView.as_view(
            template_name="workplace/calendar.html",
        ),
        name="calendar",
    ),
    path("invite_member/", views.InviteMember.as_view(), name="send_invite"),
    path("change_task/", views.change_task_state, name="change_task_state"),
    path(
        "settings/company/",
        views.CompanyProfile.as_view(),
        name="settings_company",
    ),
    path("settings/team/", views.TeamView.as_view(), name="settings_team"),
    path(
        "settings/schedule/",
        views.ScheduleView.as_view(),
        name="settings_schedule",
    ),
]
