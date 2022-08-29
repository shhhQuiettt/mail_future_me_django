from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import EmailMessage
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from . import service

# Create your tests here.


class TestService(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="q@w.com",
            password="password",
            first_name="",
            is_active=True,
        )
        # 2 mails should be sent and one not
        with patch("mailing.models.in_the_future") as mock_in_the_future:
            mock_in_the_future.return_value = True
            due_to_emails = [
                EmailMessage(
                    title="test",
                    body="qwer",
                    owner=user,
                    due_to=timezone.now().date() - timedelta(weeks=1),
                ).save(),
                EmailMessage(
                    title="test2", body="qwer", owner=user, due_to=timezone.now().date()
                ).save(),
            ]

            future_emails = [
                EmailMessage(
                    title="test",
                    body="qwer",
                    owner=user,
                    due_to=timezone.now().date() + timedelta(days=10),
                ).save()
            ]

    def test_sends_email():
        self.skipTest("Bypass model validation")
        # with patch("mailing.service.send_mail") as mock_send_mail:
        #     service.send_due_to_emails()
        #     mock_send_mail.assert_called_with("test")
