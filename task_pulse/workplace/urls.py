from django.urls import path

from stats import views as stats_views
from workplace import views as wp_views


app_name = "workplace"

urlpatterns = [
    path("tasks/", wp_views.TaskList.as_view(), name="tasks"),
    path(
        "home/",
        wp_views.HomeCompanyView.as_view(),
        name="home",
    ),
    path(
        "calendar/",
        wp_views.HomeCompanyView.as_view(
            template_name="workplace/calendar.html",
        ),
        name="calendar",
    ),
    path(
        "invite_member/",
        wp_views.InviteMember.as_view(),
        name="send_invite",
    ),
    path(
        "statistics/",
        stats_views.StatisticsListView.as_view(),
        name="statistics",
    ),
    path(
        "create_task/",
        wp_views.TaskCreationForm.as_view(),
        name="create_task",
    ),
    path(
        "create_user_statistics/",
        stats_views.CreateUserStatistics.as_view(),
        name="create_user_statistics",
    ),
    path(
        "create_company_statistics/",
        stats_views.CreateCompanyStatistics.as_view(),
        name="create_company_statistics",
    ),
    path(
        "change_task/",
        wp_views.change_task_status,
        name="change_task_status",
    ),
    path(
        "settings/company/",
        wp_views.CompanyProfile.as_view(),
        name="settings_company",
    ),
    path("settings/team/", wp_views.TeamView.as_view(), name="settings_team"),
    path(
        "settings/schedule/",
        wp_views.ScheduleView.as_view(),
        name="settings_schedule",
    ),
    path(
        "company_invite/",
        wp_views.AcceptCompanyInvite.as_view(),
        name="accept_company_invation",
    ),
]
