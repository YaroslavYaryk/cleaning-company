from rest_framework.views import APIView
from accounts.models import User
from .serializers import WorkerSerializer, FreeDatePostSerializer
from rest_framework.response import Response
from .services import handle_api
import json
from rest_framework.decorators import api_view, permission_classes
from worker.services import handle_worker
from rest_framework.permissions import IsAuthenticated
from work.api.serializers import WorkSerializer, FreeDateSerializer
from director.services import handle_work
from worker.models import FreeDates, WorkerShift
from rest_framework import status


class WorkerAPIView(APIView):
    def get(self, request, *args, **kwargs):

        queryset = User.objects.filter(admin=False)
        serializer = WorkerSerializer(queryset, many=True)
        return Response(serializer.data)


class WorkerDetailsAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):

        user = User.objects.get(pk=pk)
        serializer = WorkerSerializer(
            user,
        )
        return Response(serializer.data)


class WorkerTakenFreeDatesAPIView(APIView):
    def post(self, request, pk, *args, **kwargs):

        taken_dates, date_type = handle_api.get_taken_dates(pk, request.data)
        return Response(json.dumps({"data": taken_dates, "type": date_type}))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_worker_shifts(request, find_date):

    queryset = handle_worker.get_shift_by_user(request.user, find_date)
    serializer = WorkSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def done_shift_work(request, shift_id, worker_job_id):

    try:
        handle_worker.done_shift_work(worker_job_id)
        new_serializer = WorkSerializer(
            instance=handle_work.get_work_by_shift(
                WorkerShift.objects.get(pk=shift_id)
            ),
        )
        return Response(new_serializer.data)
    except Exception as ex:
        return Response({"message": str(ex)})


class FreeDateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        free_dates = handle_worker.get_all_free_dates(request.user)
        serializer = FreeDateSerializer(free_dates, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {**request.data, "user": request.user.id}
        print(data)
        serializer = FreeDatePostSerializer(data=data)
        if serializer.is_valid():
            try:
                instance = serializer.save()
            except Exception as ex:
                return Response({"message": str(ex)})

            return Response(serializer.data)

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        data = {**request.data, "user": request.user.id}
        instance = FreeDates.objects.get(pk=pk)
        serializer = FreeDatePostSerializer(data=data, instance=instance)
        if serializer.is_valid():
            try:
                instance = serializer.save()
            except Exception as ex:
                return Response({"message": str(ex)})

            return Response(serializer.data)

        message = "\n".join(
            [el.title() for values in serializer.errors.values() for el in values]
        )
        return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            handle_worker.delete_free_date(pk)
            return Response({"message": "success"})
        except Exception as err:
            return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class SetupDateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        free_dates = handle_worker.get_worker_setup_dates(request.user)
        serializer = FreeDateSerializer(free_dates, many=True)
        return Response(serializer.data)
