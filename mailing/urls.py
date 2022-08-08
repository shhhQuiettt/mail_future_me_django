from django.urls import path
from . import views

urlpatterns = [path("", views.MailingView.as_view(), name="mailing")]
