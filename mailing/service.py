from .models import EmailMessage
from django.utils import timezone


def send_due_to_emails():
    emails = EmailMessage.objects.filter(due_to__gte=timezone.now(), sent=False)
    for email in emails:
        email.send()
