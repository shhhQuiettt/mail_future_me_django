from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path("signup/", views.signup, name="signup"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path(
        "activate/<uidb64>/<token>",
        views.activate_account,
        name="activate_account",
    ),
    path("profile/", views.Profile.as_view(), name="profile"),
]
