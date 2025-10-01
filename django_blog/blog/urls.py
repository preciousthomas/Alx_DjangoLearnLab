# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "blog"

urlpatterns = [
    # Registration
    path("register/", views.register_view, name="register"),

    # Profile
    path("profile/", views.profile_view, name="profile"),

    # Login / Logout (using Django built-in views)
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name="logout"),
]