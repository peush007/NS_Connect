from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import ProviderProfile
from .models import Service, Review
from .forms import ReviewForm
import math

def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})

def contact(request):
    return render(request, 'contact.html')

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def service_search(request):
    # Restrict provider access
    if request.user.is_authenticated and getattr(request.user, 'role', '') == 'provider':
        return redirect('provider_dashboard')

    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    category_id = request.GET.get('category')
    radius = float(request.GET.get('radius', 50))

    providers = ProviderProfile.objects.filter(is_approved=True)
    
    if category_id:
        providers = providers.filter(service_category_id=category_id)

    results = []
    if lat and lon:
        user_lat = float(lat)
        user_lon = float(lon)
        for provider in providers:
            if provider.latitude is not None and provider.longitude is not None:
                dist = haversine(user_lat, user_lon, provider.latitude, provider.longitude)
                if dist <= radius:
                    provider.distance = round(dist, 1) 
                    results.append(provider)
        results.sort(key=lambda x: x.distance)
    else:
        results = list(providers)
        for p in results:
            p.distance = None

    context = {
        'providers': results,
        'services': Service.objects.all(),
        'selected_category': int(category_id) if category_id else None,
        'radius': radius,
        'lat': lat if lat else '',
        'lon': lon if lon else ''
    }
    return render(request, 'services/provider_list.html', context)

def provider_detail(request, pk):
    provider = get_object_or_404(ProviderProfile, pk=pk)
    user_review = None
    can_review = False
    
    if request.user.is_authenticated:
        # Check if user already reviewed this provider
        user_review = Review.objects.filter(provider=provider, user=request.user).first()
        # User can review if: logged in, not the provider themselves, and hasn't reviewed yet
        can_review = (request.user != provider.user) and (user_review is None)
    
    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.provider = provider
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('provider_detail', pk=pk)
    else:
        form = ReviewForm()
    
    context = {
        'provider': provider,
        'form': form,
        'can_review': can_review,
        'user_review': user_review,
    }
    return render(request, 'services/provider_detail.html', context)
