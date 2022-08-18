from django.urls import path
from . import views

urlpatterns = [
    path("mailing", views.MailingView.as_view(), name="mailing"),
    path("", views.AboutView.as_view(), name="about"),
]
