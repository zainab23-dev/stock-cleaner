from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, PreferenceForm
from .models import Preference

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    pref, created = Preference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=pref)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preferences updated.')
            return redirect('profile')
    else:
        form = PreferenceForm(instance=pref)
    
    return render(request, 'accounts/profile.html', {'form': form, 'preferences': pref})
