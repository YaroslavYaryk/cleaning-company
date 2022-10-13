from django.urls import re_path, path, include
from .views import (
    RoomAPIView,
    RoomWorkAPIView,
    WorkerJobAPIView,
    ShiftWorkAPIView,
    get_shift_names,
    search_worker_shift,
    get_workers_free_dates,
    get_worker_free_dates,
    approve_free_date,
    refuse_free_date,
)

urlpatterns = [
    path("rooms/", RoomAPIView.as_view()),
    path("room/create/", RoomAPIView.as_view()),
    path("room/<pk>/update/", RoomAPIView.as_view()),
    path("room/<pk>/delete/", RoomAPIView.as_view()),
    # room work
    path("room_works/", RoomWorkAPIView.as_view()),
    path("worker_jobs/", WorkerJobAPIView.as_view()),
    # shifts
    path("shift_names/", get_shift_names),
    # work
    path("works/<find_date>/", ShiftWorkAPIView.as_view()),
    path("work/create/", ShiftWorkAPIView.as_view()),
    path("work/<pk>/update/", ShiftWorkAPIView.as_view()),
    path("work/<pk>/delete/", ShiftWorkAPIView.as_view()),
    path("worker_work/<worker_email>/", search_worker_shift),
    # free dates
    path("free_dates/", get_workers_free_dates),
    path("free_dates/<email>/", get_worker_free_dates),
    path("free_date/<free_date_id>/refuse/", refuse_free_date),
    path("free_date/<free_date_id>/approve/", approve_free_date),
]
