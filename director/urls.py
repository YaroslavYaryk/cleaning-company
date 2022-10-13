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
    delete_worker_room_work,
    delete_worker_shift,
    search_worker_shift,
    get_workers_free_dates,
    approve_worker_free_date,
    refuse_worker_free_date,
    get_worker_free_dates,
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
    path("delete_shift/<shift_id>/", delete_worker_shift, name="delete_worker_shift"),
    path(
        "delete_shift_room_work/<shift_id>/<room_id>/",
        delete_worker_room_work,
        name="delete_worker_room_work",
    ),
    path(
        "workers_shifts_work_list/",
        get_workers_shifts_work_list,
        name="get_workers_shifts_work_list",
    ),
    path(
        "workers_shifts_work_list/<find_date>/",
        get_workers_shifts_work_list,
        name="get_workers_shifts_work_list",
    ),
    path(
        "workers_shifts_work_list/search/<worker_email>/",
        search_worker_shift,
        name="search_worker_shift",
    ),
    path("workers_free_date/", get_workers_free_dates, name="get_workers_free_dates"),
    path(
        "workers_free_date/<email>/",
        get_worker_free_dates,
        name="get_worker_free_dates",
    ),
    path(
        "approve_free_date/<free_date_id>/",
        approve_worker_free_date,
        name="approve_worker_free_date",
    ),
    path(
        "refuse_free_date/<free_date_id>/",
        refuse_worker_free_date,
        name="refuse_worker_free_date",
    ),
]
