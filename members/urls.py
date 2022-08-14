from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path("signup/", views.signup, name="signup"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("signup/done", views.SignUpDone.as_view(), name="signup_done"),
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
]
