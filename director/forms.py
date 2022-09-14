from work.models import Room
from django import forms
from worker.models import WorkerShift


class RoomCreate(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("name",)


class DatePickerInput(forms.DateInput):
    input_type = "date"


class TimePickerInput(forms.TimeInput):
    input_type = "time"


class DateTimePickerInput(forms.DateTimeInput):
    input_type = "datetime"


class WorkerShiftCreate(forms.ModelForm):

    date = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "class": "",
                "data-target": "#datetimepicker1",
            }
        ),
    )

    class Meta:
        model = WorkerShift
        fields = "__all__"

    def __init__(self, workers, *args, **kwargs):
        super(WorkerShiftCreate, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = workers
        self.fields["user"].empty_label = "Please select your worker"
        self.fields["shift"].empty_label = "Please select a shift"

        # self.fields["contract_template"].initial = BASE_CONTRACT
