from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Weiterleitung zur Login-Seite
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
def dashboard(request):
    return render(request, "dashboard/dashboard.html")
# Create your views here
