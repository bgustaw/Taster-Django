from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegisterUserForm, ChangePasswordForm, EditUserForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = RegisterUserForm
    form = EditUserForm
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active", "date_joined")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "username", "country", 'liked_recipes')}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2", "country", 'liked_recipes', "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
