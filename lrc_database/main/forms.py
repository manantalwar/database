from django import forms

from .models import LRCDatabaseUser, ShiftChangeRequest


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = LRCDatabaseUser
        fields = ("first_name", "last_name", "email")


class NewChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ShiftChangeRequest
        fields = ("reason", "new_associated_person", "new_start", "new_duration", "new_location")
