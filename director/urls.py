from django.urls import path
from .views import create_room, get_room_list, edit_room, delete_room_work, delete_room

urlpatterns = [
    path("create_room/", create_room, name="create_room"),
    path("rooms/", get_room_list, name="room_list"),
    path("edit_room/<room_slug>/", edit_room, name="edit_room"),
    path(
        "delete_room_work/<room_slug>/<room_work_slug>/",
        delete_room_work,
        name="delete_room_work",
    ),
    path("delete_room/<room_slug>/", delete_room, name="delete_room"),
]
