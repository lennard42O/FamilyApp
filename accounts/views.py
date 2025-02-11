from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserSettings
from .forms import UserSettingsForm

## REGISTER ##

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

## DASHBOARD ##
@login_required
def dashboard(request):
    family_members = request.user.family_members.all()
    return render(request, 'dashboard/dashboard.html', {'family_members': family_members})

## ADD FAMILY MEMBER ##
@login_required
def add_family_members(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            new_member = get_user_model().objects.get(username=username)
            request.user.family_members.add(new_member)
            return redirect("dashboard")
        except get_user_model().DoesNotExist:
            error ="Benutzer nicht gefunden."
            return render(request, "accounts/add_family_member.html", {"error: error"})
    return render(request,"accounts/add_family_member.html")
## Settings ## 
@login_required
def settings(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'change_design' in request.POST:
            settings_form = UserSettingsForm(request.POST, instance=user_settings)
            if settings_form.is_valid():
                settings_form.save()
                return redirect('settings')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Verhindert, dass der Benutzer ausgeloggt wird
                return redirect('settings')
        elif 'change_username_email' in request.POST:
            user_form = UserChangeForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('settings')
    else:
        settings_form = UserSettingsForm(instance=user_settings)
        password_form = PasswordChangeForm(request.user)
        user_form = UserChangeForm(instance=request.user)

    return render(request, 'accounts/settings.html', {
        'settings_form': settings_form,
        'password_form': password_form,
        'user_form': user_form,
    })