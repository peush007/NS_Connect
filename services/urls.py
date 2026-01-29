from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.service_search, name='service_search'),
    path('provider/<int:pk>/', views.provider_detail, name='provider_detail'),
]
