from django import forms

from .models import Course, LRCDatabaseUser, ShiftChangeRequest


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
