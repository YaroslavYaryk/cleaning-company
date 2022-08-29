from multiprocessing import context
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .services import handle_work
from .forms import RoomCreate, WorkerShiftCreate
import re
from accounts.services import handle_user
from worker.services import handle_worker

# Create your views here.


@login_required(login_url="login")
def create_room(request):

    if request.method == "POST":
        form = RoomCreate(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = slugify(room.name)
            room.save()

            keys = "/".join(request.POST.keys())
            template = r"room_work_[0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?"
            proper_keys = re.findall(template, keys)
            for key in proper_keys:
                handle_work.create_room_work(room, request.POST.get(key))
            return HttpResponseRedirect(reverse("room_list"))

    form = RoomCreate()
    context = {"form": form}
    return render(request, "director/create_room.html", context)


@login_required(login_url="login")
def get_room_list(request):
    rooms = handle_work.get_all_rooms()[0]

    context = {"rooms": rooms}

    return render(request, "director/rooms_list.html", context)


@login_required(login_url="login")
def edit_room(request, room_slug):

    room = handle_work.get_room_by_slug(room_slug)
    room_works = handle_work.get_work_for_room(room)

    if request.method == "POST":
        form = RoomCreate(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = slugify(room.name)
            room.save()
            print(request.POST)
            keys = "/".join(request.POST.keys())
            template = r"room_component_[0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?"
            proper_keys = re.findall(template, keys)
            ids = [el.split("_")[-1] for el in proper_keys]
            for key, idd in zip(proper_keys, ids):
                handle_work.edit_or_create_room_work(room, request.POST.get(key), idd)
            return HttpResponseRedirect(reverse("room_list"))

    form = RoomCreate(instance=room)
    context = {"form": form, "room_works": room_works, "room": room}
    return render(request, "director/edit_room.html", context)


@login_required(login_url="login")
def delete_room_work(request, room_slug, room_work_slug):

    try:
        handle_work.delete_room_work(room_work_slug)
    except Exception as ex:
        print(ex)

    return HttpResponseRedirect(reverse("edit_room", kwargs={"room_slug": room_slug}))


@login_required(login_url="login")
def delete_room(request, room_slug):

    try:
        handle_work.delete_room(room_slug)
    except Exception as ex:
        print(ex)

    return HttpResponseRedirect(reverse("room_list"))


@login_required(login_url="login")
def get_all_workers(request):

    workers = handle_user.get_all_workers(request.user)

    context = {"workers": workers}

    return render(request, "director/worker_list.html", context)


@login_required(login_url="login")
def create_shift(request):

    workers = handle_user.get_all_workers(request.user)

    if request.method == "POST":
        form = WorkerShiftCreate(workers, request.POST)

        if form.is_valid():
            shift = form.save()
            room_works = handle_work.get_room_work_slugs(request.POST)
            work = handle_work.create_work(shift)
            handle_work.add_room_works_to_shift(work, room_works)

            return HttpResponseRedirect(reverse("create_shift"))

    form = WorkerShiftCreate(workers)
    rooms, rooms_json = handle_work.get_all_rooms()
    room_works, room_works_json = handle_work.get_room_works()
    context = {
        "form": form,
        "rooms": rooms,
        "room_works": room_works,
        "rooms_json": rooms_json,
        "room_works_json": room_works_json,
    }

    return render(request, "director/create_shift.html", context)


@login_required(login_url="login")
def get_workers_shifts_work_list(request):

    shift_works = handle_work.get_all_shift_works()

    context = {
        "shift_works": shift_works,
    }

    return render(request, "director/workers_shifts_work_list.html", context)


@login_required(login_url="login")
def edit_shift(request, shift_id):

    workers = handle_user.get_all_workers(request.user)
    shift = handle_worker.get_shift_by_id(shift_id)
    worker_jobs_shift = handle_work.get_worker_jobs_shift(shift_id)
    works_for_category = handle_work.get_works_for_category(worker_jobs_shift)
    used_rooms = handle_work.get_free_rooms_for_work(worker_jobs_shift)

    if request.method == "POST":
        form = WorkerShiftCreate(workers, request.POST, instance=shift)

        if form.is_valid():
            handle_work.update_existed_works(shift, request.POST)

            return HttpResponseRedirect(reverse("get_workers_shifts_work_list"))

    form = WorkerShiftCreate(workers, instance=shift)
    rooms, rooms_json = handle_work.get_all_rooms()
    room_works, room_works_json = handle_work.get_room_works()
    context = {
        "form": form,
        "rooms": rooms,
        "shift": shift,
        "room_works": room_works,
        "rooms_json": rooms_json,
        "room_works_json": room_works_json,
        "worker_jobs_shift": worker_jobs_shift,
        "works_for_category": works_for_category,
        "used_rooms": used_rooms,
        "spec_name": "work_Select_",
    }
    print(room_works_json)

    return render(request, "director/edit_shift.html", context)


@login_required(login_url="login")
def delete_worker_room_work(request, shift_id, room_id):

    try:
        handle_work.delete_worker_room_work(shift_id, room_id)
    except Exception as ex:
        print(ex)

    return HttpResponseRedirect(reverse("edit_shift", kwargs={"shift_id": shift_id}))
