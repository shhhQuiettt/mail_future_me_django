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

    # Dont display inlines if form is an add form
    def get_inlines(self, request, obj):
        inl = self.inlines if obj is not None else ()
        return inl

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

    add_fieldsets = (
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
