from rest_framework.serializers import ModelSerializer
from accounts.models import User


class WorkerSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
