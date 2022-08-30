from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChangeForm
from django.contrib import messages
from worker.services import handle_worker
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy


@login_required(login_url="login")
def index(request):
    if request.user.admin:
        return render(request, "director/homepage.html")

    return render(request, "worker/homepage.html")


@login_required(login_url="login")
def get_shift_work_list(request):

    user = request.user

    shifts = handle_worker.get_shift_by_user(user)

    contex = {"shifts": shifts}

    return render(request, "worker/shift_work_list.html", contex)


@login_required(login_url="login")
def done_shift_work(request, worker_job_id):

    try:
        handle_worker.done_shift_work(worker_job_id)
    except Exception as ex:
        print(ex)

    return HttpResponseRedirect(reverse("get_shift_work_list"))
