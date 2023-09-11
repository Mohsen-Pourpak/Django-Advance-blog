from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django import forms

from accounts.models import User, Profile

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_superuser', 'is_active', 'is_verified',)
    list_filter = ('email', 'is_superuser', 'is_active', 'is_verified',)
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        ("Authentication" , {
            "fields": (
                'email', 'password'
            ),
        }),

        ('permissions', {
            "fields": (
                'is_staff', 'is_superuser', 'is_active', 'is_verified',
        ),
        }),

        ('groups', {
            'fields': (
                'groups', 'user_permissions',
            ),
        }),

        ('important date', {
            "fields": (
                'last_login', 
            ),
        }),
    )

    add_fieldsets = (
        ("Add user", {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'is_verified'),
        }),
    )


admin.site.register(Profile)
admin.site.register(User, CustomUserAdmin)