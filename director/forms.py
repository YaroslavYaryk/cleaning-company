from work.models import Room
from django import forms
from worker.models import WorkerShift


class RoomCreate(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("name",)


class WorkerShiftCreate(forms.ModelForm):
    class Meta:
        model = WorkerShift
        fields = "__all__"

    def __init__(self, workers, *args, **kwargs):
        super(WorkerShiftCreate, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = workers
        self.fields["user"].empty_label = "Please select your worker"
        self.fields["shift"].empty_label = "Please select a shift"

        # self.fields["contract_template"].initial = BASE_CONTRACT
