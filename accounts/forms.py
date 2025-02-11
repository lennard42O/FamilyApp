from django import forms
from .models import UserSettings
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser

        fields= ("username", "email", "password1","password2")
class UserSettingsForm(forms.ModelForm):
    class Meta:
        model =  UserSettings
        fields = ["design", "icons"]