from django import forms
from .models import EmailMessage
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class NewEmailForm(forms.ModelForm):
    class Meta:
        model = EmailMessage
        fields = ["title", "body"]

    PERIOD_CHOICES = [
        (1, "1 month"),
        (6, "6 months"),
        (1 * 12, "1 year"),
        (2 * 12, "2 years"),
        (5 * 12, "5 years"),
    ]

    time_period = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        # required=True,
    )

    def save(self, *args, **kwargs):
        form = super().save(commit=False)
        form.due_to = timezone.now() + relativedelta(
            months=int(self.cleaned_data["time_period"])
        )
        return super().save(*args, **kwargs)
