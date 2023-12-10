from django.urls import path
from workplace import views


app_name = "workplace"

urlpatterns = [
    path("tasks/", views.HomeCompanyView.as_view(), name="tasks"),
    path("home/", views.HomeCompanyView.as_view(), name="home"),
    path("calendar/", views.HomeCompanyView.as_view(), name="calendar"),
]
