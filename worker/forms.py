from dataclasses import fields
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm,
    ReadOnlyPasswordHashField,
    UserCreationForm,
)
from accounts.services.validators import validate_phone
from accounts.models import User
from .models import FreeDates


class ChangeForm(forms.ModelForm):

    birthdate = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control datetimepicker-input",
                "data-target": "#datetimepicker1",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "birthdate",
            "personal_number",
            "account_number",
            "is_active",
        )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        if not validate_phone(phone)[0]:
            msg = validate_phone(phone)[1]
            self.add_error("phone", msg)


class FreeDaysForm(forms.ModelForm):
    class Meta:
        model = FreeDates
        fields = ("setup_worker",)

    def __init__(self, free_setup_users, *args, **kwargs):
        super(FreeDaysForm, self).__init__(*args, **kwargs)
        self.fields["setup_worker"].queryset = free_setup_users
        self.fields["setup_worker"].empty_label = "Please select your worker"
