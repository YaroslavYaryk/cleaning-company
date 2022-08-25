from multiprocessing import context
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .services import handle_work
from .forms import RoomCreate
import re

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
    rooms = handle_work.get_all_rooms()

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
            print(proper_keys, ids)
            for key, idd in zip(proper_keys, ids):
                handle_work.edit_or_create_room_work(room, request.POST.get(key), idd)
            return HttpResponseRedirect(reverse("room_list"))

    form = RoomCreate(instance=room)
    context = {"form": form, "room_works": room_works, "room": room}
    return render(request, "director/edit_room.html", context)


def delete_room_work(request, room_slug, room_work_slug):

    try:
        handle_work.delete_room_work(room_work_slug)
    except Exception as ex:
        print(ex)

    return HttpResponseRedirect(reverse("edit_room", kwargs={"room_slug": room_slug}))


def delete_room(request, room_slug):

    try:
        handle_work.delete_room(room_slug)
    except Exception as ex:
        print(ex)

    return HttpResponseRedirect(reverse("room_list"))
