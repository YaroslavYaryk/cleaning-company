from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChangeForm
from django.contrib import messages


@login_required(login_url="login")
def index(request):
    return render(request, "worker/homepage.html")


@login_required(login_url="login")
def get_profile(request):

    user = request.user

    context = {"user": user}

    return render(request, "base/profile.html", context=context)


@login_required(login_url="login")
def get_profile_edit(request):

    user = request.user
    if request.method == "POST":
        form = ChangeForm(request.POST, instance=user)

        if form.is_valid:
            try:
                form.save()
            except Exception as er:
                messages.error(request, er)

    form = ChangeForm(instance=user)

    context = {"user": user, "form": form}

    return render(request, "base/profile_edit.html", context=context)
