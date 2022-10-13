from rest_framework.serializers import ModelSerializer
from accounts.models import User
from worker.models import FreeDates, WorkerShift
from django.core.exceptions import ValidationError


class WorkerSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class FreeDatePostSerializer(ModelSerializer):
    class Meta:
        model = FreeDates
        exclude = ("approved",)

    @staticmethod
    def user_date_taken_as_word_day(user, date1, date2):
        my_shifts = WorkerShift.objects.filter(user=user)
        for dates in my_shifts:

            if WorkerShift.is_overlapped(
                [date1, date2],
                [
                    dates.date,
                    dates.date,
                ],
            ):
                return True

    def save(self, *args, **kwargs):
        user = self.validated_data["user"]
        setup_worker = self.validated_data["setup_worker"]

        start_date = self.validated_data["start_date"]
        end_date = self.validated_data["end_date"]

        if WorkerShift.user_date_taken_as_setup_date(user, start_date, end_date):
            raise ValidationError("This user is a setup for another user")
        if WorkerShift.user_date_taken_as_free_date(user, start_date, end_date):
            raise ValidationError("This user has a free day this date")
        if FreeDatePostSerializer.user_date_taken_as_word_day(
            user, start_date, end_date
        ):
            raise ValidationError("This user already has a work during this period")

        if setup_worker:
            if WorkerShift.user_date_taken_as_setup_date(
                setup_worker, start_date, end_date
            ):
                raise ValidationError("This setup worker is a setup for another user")
            if WorkerShift.user_date_taken_as_free_date(
                setup_worker, start_date, end_date
            ):
                raise ValidationError("This setup worker has a free day this date")
            if FreeDatePostSerializer.user_date_taken_as_word_day(
                setup_worker, start_date, end_date
            ):
                raise ValidationError(
                    "This setup worker already has a work during this period"
                )
        super(FreeDatePostSerializer, self).save(*args, **kwargs)
