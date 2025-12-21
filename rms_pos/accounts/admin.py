from django.contrib import admin
from .models import User, ReferenceCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'created_by', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']


@admin.register(ReferenceCode)
class ReferenceCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'role_for', 'created_by', 'is_used', 'used_by', 'created_at', 'expires_at']
    list_filter = ['role_for', 'is_used']
    search_fields = ['code', 'created_by__username', 'used_by__username']
    readonly_fields = ['code', 'is_used', 'used_by', 'created_at']

