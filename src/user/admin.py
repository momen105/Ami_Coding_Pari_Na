from django.contrib import admin
from user import models
from django.contrib.auth.admin import UserAdmin


class AdminUser(UserAdmin):
    ordering = ("-id",)
    search_fields = ("username",)
    list_filter = ("is_active", "is_staff", "is_superuser")
    list_display = ("username", "id", "is_active")
    fieldsets = (
        ("Login Info", {"fields": ("username", "password")}),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )


admin.site.register(models.User, AdminUser)
admin.site.register(models.SearchModel)
