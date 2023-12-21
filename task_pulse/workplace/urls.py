from django.urls import path
from django.views import generic

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
        generic.TemplateView.as_view(
            template_name="workplace/calendar.html",
        ),
        name="calendar",
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
]
