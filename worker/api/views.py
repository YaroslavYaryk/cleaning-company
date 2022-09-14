from rest_framework.views import APIView
from accounts.models import User
from .serializers import WorkerSerializer
from rest_framework.response import Response
from .services import handle_api
import json


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
