from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages


from .forms import CreateUserForm
from .utils import send_confirmation_mail, activate_user


class SignUp(FormView):
    template_name = "registration/signup.html"
    form_class = CreateUserForm
    success_url = "/accounts/signup/done"  # reverse_lazy("signup_done")

    def form_valid(self, form):
        # TODO: How can I obtain user from FormView instead of saving and fetching it again?
        form.save()
        email = form.data.get("email")
        send_confirmation_mail(
            user=get_object_or_404(get_user_model(), email=email),
            domain=self.request.META["HTTP_HOST"],
        )
        messages.add_message(
            self.request, messages.INFO, f"Veryfication email has been sent to {email}"
        )

        return super().form_valid(form)


class SignUpDone(TemplateView):
    template_name = "registration/signup_done.html"


def activate_account(request, uidb64, token):
    err = activate_user(uidb64=uidb64, token=token)

    message, level = (
        "Email confirmed! Now you can log in",
        message.INFO if err is not None else err,
        messages.ERROR,
    )
    messages.add_message(request, level, message)

    return redirect(reverse("login"))
