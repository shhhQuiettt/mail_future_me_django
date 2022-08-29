from django.db import models
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from .validators import in_the_future
from django.contrib.auth import get_user_model


class EmailMessage(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    due_to = models.DateField(validators=[in_the_future])
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Email Message for {self.owner.email} ({self.pk})"

    def save(self):
        self.full_clean()
        return super().save()

    def send(self):
        is_sent = send_mail(
            subject=self.title,
            message=self.body,
            from_email=None,
            recipient_list=[self.owner.email],
        )
        self.sent = is_sent
