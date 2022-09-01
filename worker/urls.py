from django.urls import path
from .views import (
    get_shift_work_list,
    done_shift_work,
    add_free_days,
    get_free_days_list,
)

urlpatterns = [
    path("shifts/", get_shift_work_list, name="get_shift_work_list"),
    path("<worker_job_id>/done/", done_shift_work, name="done_shift_work"),
    path("add_free_days/", add_free_days, name="add_free_days"),
    path("free_dates_list/", get_free_days_list, name="get_free_days_list"),
]
