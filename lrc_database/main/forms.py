from django import forms

from .models import Course, Hardware, Loan, LRCDatabaseUser, ShiftChangeRequest


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("department", "number", "name")


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = LRCDatabaseUser
        fields = ("first_name", "last_name", "email")


class NewChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ShiftChangeRequest
        fields = (
            "reason",
            "new_associated_person",
            "new_start",
            "new_duration",
            "new_location",
        )


class AddHardwareForm(forms.ModelForm):
    class Meta:
        model = Hardware
        fields = ("name", "is_available")

        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class NewLoanForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            format="%d/%m/%Y %H:%M", attrs={"class": "form-control"}
        ),
        help_text="DD/MM/YYYY HH:MM",
    )
    return_time = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            format="%d/%m/%Y %H:%M", attrs={"class": "form-control"}
        ),
        required=False,
        help_text="DD/MM/YYYY HH:MM",
    )
    target = forms.Select(attrs={"class": "form-control"})
    hardware_user = forms.Select(attrs={"class": "form-control"})

    class Meta:
        model = Loan
        fields = ("target", "hardware_user", "start_time", "return_time")
