from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProviderProfileForm
from .models import ProviderProfile

def register_provider_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProviderProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'provider'
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.is_approved = False
            profile.save()
            
            profile_form.save_m2m()
            
            login(request, user)
            return redirect('provider_dashboard')
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProviderProfileForm()
        
    return render(request, 'users/register_provider.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'provider':
                return redirect('provider_dashboard')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'provider':
                return redirect('provider_dashboard')
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def provider_dashboard_view(request):
    return render(request, 'users/provider_dashboard.html')
