from django.urls import path
from .views import (
    create_room,
    get_room_list,
    edit_room,
    delete_room_work,
    delete_room,
    get_all_workers,
    create_shift,
    get_workers_shifts_work_list,
    edit_shift,
)

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
    path("workers/", get_all_workers, name="get_all_workers"),
    path("create_shift/", create_shift, name="create_shift"),
    path("edit_shift/<shift_id>/", edit_shift, name="edit_shift"),
    path(
        "workers_shifts_work_list/",
        get_workers_shifts_work_list,
        name="get_workers_shifts_work_list",
    ),
]
