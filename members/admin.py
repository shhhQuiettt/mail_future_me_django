from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mailing.models import EmailMessage
from .models import User


class EmailMessageAdminInline(admin.StackedInline):
    model = EmailMessage
    fields = ("title", "due_to")


class UserAdminConfig(UserAdmin):
    search_fields = ("email", "first_name")
    ordering = ("-created_at",)
    list_display = ("email", "created_at")
    list_filter = ("is_active", "is_staff", "is_superuser")

    inlines = (EmailMessageAdminInline,)

    fieldsets = (
        (
            None,
            {
                "fields": ("email", "first_name"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "user_permissions",
                    "groups",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(User, UserAdminConfig)
