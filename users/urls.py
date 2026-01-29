from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register-provider/', views.register_provider_view, name='register_provider'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.provider_dashboard_view, name='provider_dashboard'),
    path('my-dashboard/', views.user_dashboard_view, name='user_dashboard'),
]
