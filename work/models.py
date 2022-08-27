from django.db import models
from worker.models import WorkerShift

# Create your models here.
class Room(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL", null=True
    )

    def __str__(self):
        return self.name


class RoomWork(models.Model):

    room = models.ForeignKey(Room, verbose_name=("room"), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL", null=True
    )

    def __str__(self):
        return f"{self.room} - {self.name}"


class WorkerJob(models.Model):
    room_work = models.ForeignKey(
        RoomWork, verbose_name=("room_work"), on_delete=models.CASCADE
    )
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room_work.name} - {self.done}"


class Work(models.Model):

    worker_job = models.ManyToManyField(WorkerJob, verbose_name=("worker_job"))

    worker_shift = models.ForeignKey(
        WorkerShift, verbose_name=("worker"), on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.worker_shift.user} - {self.worker_shift.shift}"
