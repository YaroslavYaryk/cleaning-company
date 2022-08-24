from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChangeForm
from django.contrib import messages


@login_required(login_url="login")
def index(request):
    if request.user.admin:
        return render(request, "director/homepage.html")

    return render(request, "worker/homepage.html")
