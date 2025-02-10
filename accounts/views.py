from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login


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
    return render(request, "dashboard/dashboard.html")

def profile(request):
    return render(request, "account/profile.html")
