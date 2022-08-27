from django.contrib import admin
from .models import Room, RoomWork, Work, WorkerJob

# Register your models here.

admin.site.register(Room)
admin.site.register(RoomWork)
admin.site.register(Work)
admin.site.register(WorkerJob)
