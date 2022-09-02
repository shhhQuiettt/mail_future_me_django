from celery import shared_task
from typing import List
from django.core.mail import EmailMultiAlternatives


@shared_task(ignore_result=True)
def send_mail(
    *,
    subject: str,
    text_body: str,
    html_body: str = None,
    from_email: str = None,
    to: List[str],
    **kwargs
):
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to,
        **kwargs,
    )
    if html_body is not None:
        email.attach_alternative(html_body, "text/html")

    email.send()
