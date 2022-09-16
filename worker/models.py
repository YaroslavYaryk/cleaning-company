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
