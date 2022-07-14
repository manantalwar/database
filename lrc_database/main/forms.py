from django import forms
from django.contrib.auth.models import Group

from .models import Course, LRCDatabaseUser, ShiftChangeRequest


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
