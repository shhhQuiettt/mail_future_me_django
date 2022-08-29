from django.contrib.auth.mixins import (
    LoginRequiredMixin as DjangoLoginRequiredMixin,
    UserPassesTestMixin as DjangoUserPassesTestMixin,
)
from django.contrib import messages
from django.shortcuts import redirect


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    permission_denied_message = "You have to log in first"

    def handle_no_permission(self):
        messages.add_message(
            self.request, messages.ERROR, self.permission_denied_message
        )
        return super().handle_no_permission()


class LogoutRequiredMixin(DjangoUserPassesTestMixin):
    test_func = lambda self: not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("mailing")
