from django.shortcuts import render, redirect
from .forms import CreateUserForm

from django.urls import reverse
from django.contrib import messages

# Create your views here.


def signup(request):

    if request.user.is_authenticated:
        return redirect(reverse("mailing"))

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.INFO,
                f"Account has been created for {form.cleaned_data.get('username')}",
            )
            return redirect("login")

    context = {"form": form}
    return render(request, "registration/signup.html", context)
