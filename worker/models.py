from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class WorkerShift(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    SHIFT_NAMES = (
        ("morning shift", "morning shift"),
        ("day shift", "day shift"),
        ("evening shift", "evening shift"),
        ("night shift", "night shift"),
    )

    shift = models.CharField(max_length=100, choices=SHIFT_NAMES)

    date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "shift", "date")

    def __str__(self):
        return f"{self.user} - {self.shift}"

    def save(self, *args, **kwargs):
        if WorkerShift.user_date_taken_as_setup_date(self.user, self.date, self.date):
            raise ValidationError("This user is a setup for another user")
        if WorkerShift.user_date_taken_as_free_date(self.user, self.date, self.date):
            raise ValidationError("This user has a free day this date")
        super(WorkerShift, self).save(*args, **kwargs)

    @staticmethod
    def is_overlapped(range_1, time_range):
        return max(range_1[0], time_range[0]) <= min(range_1[1], time_range[1])

    @staticmethod
    def user_date_taken_as_free_date(user, date1, date2):
        my_free_dates = FreeDates.objects.filter(user=user, approved=True)
        for dates in my_free_dates:

            if WorkerShift.is_overlapped(
                [date1, date2],
                [
                    dates.start_date,
                    dates.end_date,
                ],
            ):
                return True

    @staticmethod
    def user_date_taken_as_setup_date(user, date1, date2):
        my_setup_dates = FreeDates.objects.filter(setup_worker=user, approved=True)
        for dates in my_setup_dates:

            if WorkerShift.is_overlapped(
                [date1, date2],
                [
                    dates.start_date,
                    dates.end_date,
                ],
            ):
                return True

    def clean(self, *args, **kwargs):
        if self.user.admin:
            raise ValidationError("Admin cannot have shift")
        super(WorkerShift, self).clean(*args, **kwargs)


class FreeDates(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    setup_worker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="setup_worker",
        blank=True,
        null=True,
    )

    approved = models.CharField(max_length=100, default="null")

    class Meta:
        unique_together = ("user", "start_date", "end_date")

    def __str__(self):
        return f"{self.user.email} - {self.start_date} - {self.end_date} - (setup)-{self.setup_worker} - {self.approved}"
