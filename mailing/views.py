from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from .permissions import LoginRequiredMixin
from .forms import NewEmailForm
from members.forms import CreateUserForm

# Create your views here.


class MailingView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "mailing/mailing.html"
    form_class = NewEmailForm
    success_url = reverse_lazy("mailing")
    # TODO: Change to show message in years too
    success_message = "Mail has been sent to you in %(time_period)s months!"

    def form_valid(self, form):
        mail = form.save(commit=False)
        mail.owner = self.request.user
        mail.save()
        return super().form_valid(form)
