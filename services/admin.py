from django.contrib import admin
from .models import Service, Review

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('provider', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('provider__user__username', 'user__username', 'comment')
