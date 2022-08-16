from django import forms
from .models import EmailMessage


class NewEmailForm(forms.ModelForm):
    class Meta:
        model = EmailMessage
        fields = ["title", "body", "due_to"]
        widgets = {"due_to": forms.DateInput(attrs={"type": "date"})}

    # PERIOD_CHOICES = [
    #     (1, "1 month"),
    #     (6, "6 months"),
    #     (1 * 12, "1 year"),
    #     (2 * 12, "2 years"),
    #     (5 * 12, "5 years"),
    # ]

    # time_periodd = forms.ChoiceField(choices=PERIOD_CHOICES, required=True)
