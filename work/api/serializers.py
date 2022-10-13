from worker.models import FreeDates, WorkerShift
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from work.models import Room, RoomWork, Work, WorkerJob


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class RoomPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("name",)


class RoomWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomWork
        fields = "__all__"


class WorkerJobSerializer(serializers.ModelSerializer):

    room_work = RoomWorkSerializer()

    class Meta:
        model = WorkerJob
        fields = "__all__"


class WorkerShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerShift
        fields = "__all__"


class WorkSerializer(serializers.ModelSerializer):

    worker_shift = WorkerShiftSerializer()
    worker_job = WorkerJobSerializer(many=True)

    class Meta:
        model = Work
        fields = "__all__"


class FreeDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeDates
        fields = "__all__"
