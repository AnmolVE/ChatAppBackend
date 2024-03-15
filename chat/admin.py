from django.contrib import admin

from .models import (
    NewUser,
)

from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    model = NewUser
    list_display = (
        "id",
        "email",
        "username",
        "get_image",
        "is_active",
        "is_staff",
    )
    list_filter = ("email", "username", "is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "image")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "image",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("-start_date",)

admin.site.register(NewUser, UserAdminConfig)
