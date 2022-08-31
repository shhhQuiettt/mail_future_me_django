import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mail_future_me.settings")

app = Celery("mail_future_me")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
