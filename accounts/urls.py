from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register, dashboard, add_family_members, settings, e404

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html"),name = "login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("", dashboard, name="dashboard"),
    path('add-family-member/', add_family_members, name='add-family-member'),
    path("settings", settings, name="settings")



]