from worker.models import FreeDates, WorkerShift
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from work.models import Room, RoomWork, Work, WorkerJob
from .serializers import (
    FreeDateSerializer,
    RoomSerializer,
    RoomPostSerializer,
    RoomWorkSerializer,
    WorkSerializer,
    WorkerJobSerializer,
    WorkerShiftSerializer,
)
from rest_framework.decorators import api_view, permission_classes

from .services import handle_work_api
from director.services import handle_work
from worker.services import handle_worker


class RoomAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Room.objects.all()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = RoomPostSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            handle_work_api.add_work_to_room(instance, request.data.get("works"))
            new_serializer = RoomSerializer(instance=instance)
            return Response(new_serializer.data)
        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        instance = Room.objects.get(pk=pk)
        serializer = RoomPostSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            instance = serializer.save()
            new_serializer = RoomSerializer(instance=instance)
            return Response(new_serializer.data)
        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = Room.objects.get(pk=pk)

        try:
            data = {"id": instance.id, "message": "successful"}
            instance.delete()
            return Response(data)
        except Exception as ex:
            return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


class RoomWorkAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = RoomWork.objects.all()
        serializer = RoomWorkSerializer(queryset, many=True)
        return Response(serializer.data)


class WorkerJobAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = WorkerJob.objects.all()
        serializer = WorkerJobSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_shift_names(request):

    names = handle_work_api.get_shift_names()

    return Response(names)


class ShiftWorkAPIView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, find_date):
        queryset = handle_work.get_all_shift_works(find_date)
        serializer = WorkSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):

        serializer = WorkerShiftSerializer(data=request.data)
        if serializer.is_valid():
            try:
                shift = serializer.save()
            except Exception as ex:
                return Response({"message": str(ex)})
            work = handle_work.create_work(shift)
            handle_work.add_room_works_to_shift(work, request.data.get("room_works"))

            new_serializer = WorkSerializer(work)
            return Response(new_serializer.data)

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        instance = WorkerShift.objects.get(pk=pk)
        serializer = WorkerShiftSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            try:
                shift = serializer.save()
            except Exception as ex:
                return Response({"message": str(ex)})
            work = handle_work.get_work_by_shift(shift)
            if request.data.get("changed"):
                handle_work_api.update_existed_works(
                    shift, request.data.get("room_works")
                )

            new_serializer = WorkSerializer(work)
            return Response(new_serializer.data)

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            handle_work.delete_whole_worker_shift(pk)
            return Response({"message": "success"})
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def search_worker_shift(request, worker_email):

    shift_works = handle_work.get_searched_shifts(worker_email)

    serializer = WorkSerializer(shift_works, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_workers_free_dates(request):

    free_dates = handle_worker.get_workers_free_dates()

    serializer = FreeDateSerializer(free_dates, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def get_worker_free_dates(request, email):

    free_dates = handle_worker.get_worker_free_dates(email.strip())

    serializer = FreeDateSerializer(free_dates, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def approve_free_date(request, free_date_id):

    try:
        handle_worker.approve_free_date(free_date_id)
        serializer = FreeDateSerializer(instance=FreeDates.objects.get(pk=free_date_id))
        return Response(serializer.data)
    except Exception as ex:
        return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAdminUser])
def refuse_free_date(request, free_date_id):

    try:
        handle_worker.refuse_free_date(free_date_id)
        serializer = FreeDateSerializer(instance=FreeDates.objects.get(pk=free_date_id))
        return Response(serializer.data)
    except Exception as ex:
        return Response({"message": str(ex)}, status=status.HTTP_400_BAD_REQUEST)
