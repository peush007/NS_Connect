from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProviderProfileForm, SinglePasswordUserCreationForm
from .models import ProviderProfile

def register_provider_view(request):
    if request.method == 'POST':
        # Use simple single-password form
        user_form = SinglePasswordUserCreationForm(request.POST)
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
            
            # success message with explicit approval info
            messages.success(request, "Your registration request has been sent to the admin. Once the admin approves your request, your profile will be visible to users.")
            
            # Log usage but redirect to dashboard as requested
            login(request, user)
            return redirect('provider_dashboard')
    else:
        user_form = SinglePasswordUserCreationForm()
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
            return redirect('user_dashboard')
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
            return redirect('user_dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def provider_dashboard_view(request):
    if request.user.role != 'provider':
        return redirect('user_dashboard')
    
    try:
        profile = request.user.provider_profile
    except ProviderProfile.DoesNotExist:
        profile = None
        
    return render(request, 'users/provider_dashboard.html', {'profile': profile})

@login_required
def user_dashboard_view(request):
    if request.user.role == 'provider':
        return redirect('provider_dashboard')
    return render(request, 'users/user_dashboard.html')
