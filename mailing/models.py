from django.db import models
from django.contrib.auth import get_user_model


class EmailMessage(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    due_to = models.DateField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
