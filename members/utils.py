import logging

import six
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User

logger = logging.getLogger(__name__)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


def send_confirmation_mail(*, user: User, domain: str) -> None:
    account_activation_token = TokenGenerator()
    context = {
        "token": account_activation_token.make_token(user),
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "domain": domain,
    }

    mail_subject = "Activate your account"
    mail_body = render_to_string("registration/mails/confirmation_mail.html", context)
    to_email = user.email

    email_message = EmailMultiAlternatives(
        subject=mail_subject,
        body=mail_body,
        to=[to_email],
    )
    email_message.attach_alternative(mail_body, "text/html")
    is_email_sent = email_message.send()

    if is_email_sent == 0:
        logger.error(f"Confirmation email not sent to {to_email}")


def activate_user(*, uidb64, token):
    account_activation_token = TokenGenerator()

    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(), pk=uid)

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return None

    return "Invalid activation token"

