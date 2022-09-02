from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ChangeForm, FreeDaysForm
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


@login_required(login_url="login")
def add_free_days(request):

    free_setup_users = handle_worker.get_free_setup_users(request.user)
    form = FreeDaysForm(free_setup_users)
    if request.method == "POST":
        form = FreeDaysForm(free_setup_users, request.POST)
        if form.is_valid():
            try:
                # print(bool(request.POST.get("setup_worker")))
                # if handle_worker.is_avaluable_date_for_worker(request.POST):
                #     pass
                free_dates = form.save(commit=False)
                free_dates.user = request.user
                handle_worker.add_dates_to_free_dates(
                    free_dates, request.POST["datepicker"]
                )
            except Exception as ex:
                print(ex)
            # dates = request.POST["datepicker"].split("to")
            # first, second = dates[0].strip(), dates[1].strip()
            return HttpResponseRedirect(reverse("get_free_days_list"))

    context = {"form": form}

    return render(request, "worker/add_free_days.html", context)


@login_required(login_url="login")
def get_free_days_list(request):

    free_dates = handle_worker.get_all_free_dates(request.user)

    context = {"free_dates": free_dates}

    return render(request, "worker/free_dates_list.html", context)


@login_required(login_url="login")
def edit_free_days(request, free_day_id):

    free_setup_users = handle_worker.get_free_setup_users(request.user)
    free_date = handle_worker.get_dree_day_by_id(free_day_id)
    form = FreeDaysForm(free_setup_users, instance=free_date)
    if request.method == "POST":
        form = FreeDaysForm(free_setup_users, request.POST, instance=free_date)
        if form.is_valid():
            try:
                free_dates = form.save(commit=False)
                free_dates.user = request.user
                handle_worker.add_dates_to_free_dates(
                    free_dates, request.POST["datepicker"]
                )
            except Exception as ex:
                print(ex)
            # dates = request.POST["datepicker"].split("to")
            # first, second = dates[0].strip(), dates[1].strip()
            return HttpResponseRedirect(reverse("get_free_days_list"))

    context = {
        "form": form,
        "free_date": free_date,
        "dates_list": handle_worker.get_data_list(free_date),
    }
    print(handle_worker.get_data_list(free_date))

    return render(request, "worker/edit_free_dates.html", context)


@login_required(login_url="login")
def get_setup_dates_list(request):

    setup_days = handle_worker.get_worker_setup_dates(request.user)

    context = {"setup_days": setup_days}

    return render(request, "worker/setup_dates_list.html", context)
