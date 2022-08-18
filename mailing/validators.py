from django.utils import timezone
from django.core.exceptions import ValidationError


def in_the_future(value):
    if value <= timezone.now().date():
        raise ValidationError("Date is not in the future")
