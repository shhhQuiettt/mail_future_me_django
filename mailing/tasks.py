from .models import EmailMessage
from django.utils import timezone
from celery import shared_task, group


# TODO: There should be more efficient way
@shared_task
def send_due_to_emails():
    emails = EmailMessage.objects.filter(due_to__lte=timezone.now().date(), sent=False)
    for email in emails:
        is_sent = email.send()
        if is_sent:
            email.sent = True
            email.save(force_update=True)
