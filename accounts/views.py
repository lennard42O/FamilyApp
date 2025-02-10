from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
def dashboard(request):
    family_members = request.user.family_members.all()
    return render(request, 'dashboard/dashboard.html', {'family_members': family_members})
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