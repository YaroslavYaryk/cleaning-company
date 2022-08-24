from multiprocessing import context
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from .forms import RoomCreate

# Create your views here.


@login_required(login_url="login")
def create_room(request):

    if request.method == "POST":
        form = RoomCreate(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = slugify(room.name)
            room.save()
            return HttpResponseRedirect(reverse("home"))

    form = RoomCreate()
    context = {"form": form}
    return render(request, "director/create_room.html", context)
