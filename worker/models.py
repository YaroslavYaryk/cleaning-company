from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class WorkerShift(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    SHIFT_NAMES = (
        ("morning_shift", "morning shift"),
        ("day_shift", "day shift"),
        ("evening_shift", "evening shift"),
        ("night_shift", "night shift"),
    )

    shift = models.CharField(max_length=100, choices=SHIFT_NAMES)

    def __str__(self):
        return f"{self.user} - {self.shift}"

    def clean(self, *args, **kwargs):
        if self.user.admin:
            raise ValidationError("Admin cannot have shift")
        super(WorkerShift, self).clean(*args, **kwargs)
