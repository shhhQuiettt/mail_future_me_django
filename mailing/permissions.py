from django.contrib.auth.mixins import LoginRequiredMixin as DjangoLoginRequiredMixin
from django.contrib import messages


class LoginRequiredMixin(DjangoLoginRequiredMixin):
    permission_denied_message = "You have to log in first"

    def handle_no_permission(self):
        messages.add_message(
            self.request, messages.ERROR, self.permission_denied_message
        )
        return super().handle_no_permission()
