from work.models import Room
from django import forms


class RoomCreate(forms.ModelForm):
    class Meta:
        model = Room
        fields = ("name",)
