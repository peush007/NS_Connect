from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ProviderProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'service_category', 'phone_number', 'is_approved', 'latitude', 'longitude')
    list_filter = ('is_approved', 'service_category')
    search_fields = ('user__username', 'user__email', 'full_name', 'service_category__name')
    actions = ['approve_providers']

    @admin.action(description='Approve selected providers')
    def approve_providers(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} providers were successfully approved.', messages.SUCCESS)

admin.site.register(CustomUser, CustomUserAdmin)
