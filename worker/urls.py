from django.urls import path
from .views import get_shift_work_list, done_shift_work

urlpatterns = [
    path("shifts/", get_shift_work_list, name="get_shift_work_list"),
    path("<worker_job_id>/done/", done_shift_work, name="done_shift_work"),
]
