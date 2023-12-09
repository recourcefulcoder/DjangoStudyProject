from django.contrib.auth import views as auth_views
from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("my_companies/", views.UserCompaniesView.as_view(), name="companies"),
    path(
        "settings/<int:pk>/",
        views.UserChangeView.as_view(),
        name="profile",
    ),
    path(
        "new_company/",
        views.CreateCompanyView.as_view(),
        name="create_company",
    ),
]
