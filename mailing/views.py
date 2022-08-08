from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.


class MailingView(TemplateView):
    template_name = "mailing/base.html"
