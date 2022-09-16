from django.urls import path, include
from .views import (
    get_shift_work_list,
    done_shift_work,
    add_free_days,
    get_free_days_list,
    edit_free_days,
    get_setup_dates_list,
)
from .api import urls as worker_api

urlpatterns = [
    path("api/", include(worker_api)),
    path("shifts/<find_date>/", get_shift_work_list, name="get_shift_work_list"),
    path("<worker_job_id>/done/", done_shift_work, name="done_shift_work"),
    path("add_free_days/", add_free_days, name="add_free_days"),
    path("free_dates_list/", get_free_days_list, name="get_free_days_list"),
    path("setup_dates_list/", get_setup_dates_list, name="get_setup_dates_list"),
    path("edit_free_days/<free_day_id>/", edit_free_days, name="edit_free_days"),
]
