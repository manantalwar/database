from django import forms
from django.contrib.auth.models import Group

from .models import Course, Hardware, Loan, LRCDatabaseUser, Shift, ShiftChangeRequest


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("department", "number", "name")


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = LRCDatabaseUser
        fields = ("username", "email", "first_name", "last_name", "password", "courses_tutored", "si_course")

    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)


class CreateUsersInBulkForm(forms.Form):
    user_data = forms.CharField(widget=forms.Textarea)


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = LRCDatabaseUser
        fields = ("first_name", "last_name", "email")


class ApproveChangeRequestForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ("associated_person", "start", "duration", "location", "kind")


class NewChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ShiftChangeRequest
        fields = ("reason", "new_start", "new_duration", "new_location", "new_kind")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["new_start"].widget = forms.DateTimeInput()


class NewDropRequestForm(forms.ModelForm):
    class Meta:
        model = ShiftChangeRequest
        fields = ("reason",)


class AddHardwareForm(forms.ModelForm):
    class Meta:
        model = Hardware
        fields = ("name", "is_available")
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class NewShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        exclude = ()


class NewShiftForTutorForm(forms.ModelForm):
    class Meta:
        model = Shift
        exclude = ("associated_person", "location", "kind")


class NewLoanForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(format="%d/%m/%Y %H:%M", attrs={"class": "form-control"}),
        help_text="DD/MM/YYYY HH:MM",
    )
    return_time = forms.DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(format="%d/%m/%Y %H:%M", attrs={"class": "form-control"}),
        required=False,
        help_text="DD/MM/YYYY HH:MM",
    )
    target = forms.Select(attrs={"class": "form-control"})
    hardware_user = forms.Select(attrs={"class": "form-control"})

    class Meta:
        model = Loan
        fields = ("target", "hardware_user", "start_time", "return_time")
