from django.urls import path

from .views import WorkerAPIView, WorkerDetailsAPIView, WorkerTakenFreeDatesAPIView

urlpatterns = [
    path("worker_list/", WorkerAPIView.as_view()),
    path("worker_list/<pk>/", WorkerDetailsAPIView.as_view()),
    path("worker/<pk>/taken_free_dates/", WorkerTakenFreeDatesAPIView.as_view()),
]
