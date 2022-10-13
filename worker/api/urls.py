from django.urls import path

from .views import (
    WorkerAPIView,
    WorkerDetailsAPIView,
    WorkerTakenFreeDatesAPIView,
    get_worker_shifts,
    done_shift_work,
    FreeDateAPIView,
    SetupDateAPIView,
)

urlpatterns = [
    path("worker_list/", WorkerAPIView.as_view()),
    path("worker_list/<pk>/", WorkerDetailsAPIView.as_view()),
    path("worker/<pk>/taken_free_dates/", WorkerTakenFreeDatesAPIView.as_view()),
    # shifts
    path("worker_shifts/<find_date>/", get_worker_shifts),
    path("shift/<shift_id>/work/<worker_job_id>/done/", done_shift_work),
    # free dates
    path("free_days/", FreeDateAPIView.as_view()),
    path("free_day/create/", FreeDateAPIView.as_view()),
    path("free_day/<pk>/update/", FreeDateAPIView.as_view()),
    path("free_day/<pk>/delete/", FreeDateAPIView.as_view()),
    # setup worker
    path("setup_dates/", SetupDateAPIView.as_view()),
]
