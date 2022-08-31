from typing import Union

import six
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User
from . import tasks


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


# TODO: It shouldnt have domain arg
def send_confirmation_mail(*, user: User, domain: str) -> None:
    activation_link = _generate_account_activation_link(user=user, domain=domain)

    mail_subject = "Activate your account"
    mail_text_body = f"Activation link: {activation_link}"
    mail_html_body = _render_account_activation_email_message(
        context={"activation_link": activation_link}
    )
    to_email = user.email

    tasks.send_mail.delay(
        subject=mail_subject,
        text_body=mail_text_body,
        html_body=mail_html_body,
        to=[to_email],
    )


def _generate_account_activation_link(*, user: User, domain: str) -> str:
    token = _generate_account_activation_token(user=user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"http://{domain}{reverse('activate_account', kwargs = {'uidb64': uidb64, 'token': token})}"
    return activation_link


def _generate_account_activation_token(*, user: User) -> str:
    token_generator = TokenGenerator()
    return token_generator.make_token(user)


def _render_account_activation_email_message(context: dict) -> str:
    return render_to_string("registration/mails/confirmation_mail.html", context)


def activate_user(*, uidb64, token) -> None:
    account_activation_token = TokenGenerator()

    user = _get_user_from_uidb64(uidb64)

    if account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return None

    raise ValueError("Invalid token")


def _get_user_from_uidb64(uidb64: Union[bytes | str]) -> User:
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(get_user_model(), pk=uid)
    return user
