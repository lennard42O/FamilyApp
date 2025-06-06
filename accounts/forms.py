from django import forms
from django.contrib.auth import get_user_model
from .models import UserSettings
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .models import CustomUser 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields= ("username", "email", "password1","password2")

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']  


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model =  UserSettings
        fields = ["design"]
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
    