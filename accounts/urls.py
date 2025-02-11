from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import register
from .views import dashboard
from .views import add_family_members
from .views import settings

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html"),name = "login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path('add-family-member/', add_family_members, name='add-family-member'),
    path("", dashboard, name="dashboard"),
    path("settings", settings, name="settings")



]