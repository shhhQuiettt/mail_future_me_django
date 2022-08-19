from django.contrib import admin
from .models import EmailMessage

# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = ("__str__", "due_to")


admin.site.register(EmailMessage, EmailAdmin)
