from django.urls import path
from . import views
from django.contrib.auth import views as django_auth_views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "activate/<uidb64>/<token>",
        views.activate_account,
        name="activate_account",
    ),
    path("profile/", views.Profile.as_view(), name="profile"),
]
