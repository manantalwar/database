from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class Course(models.Model):
    department = models.CharField(
        max_length=16,
        help_text="Department string, like COMPSCI or MATH.",
    )
    number = models.IntegerField(
        validators=[
            validators.MinValueValidator(100),
            validators.MaxValueValidator(999),
        ],
        help_text="Course number, like the 187 in COMPSCI 187.",
    )
    name = models.CharField(
        max_length=64,
        help_text='The human-legible name of the course, like "Programming with Data Structures."',
    )

    def __str__(self):
        return f"{self.department} {self.number}: {self.name}"


class LRCDatabaseUser(AbstractUser):
    courses_tutored = models.ManyToManyField(Course, blank=True, default=None)
    si_course = models.ForeignKey(
        to=Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        related_name="lrc_database_user_si_course",
        verbose_name="SI course",
    )

    def __str__(self):
        if not (self.first_name and self.last_name):
            return self.username
        else:
            return f"{self.first_name} {self.last_name}"


class Shift(models.Model):
    associated_person = models.ForeignKey(
        to=LRCDatabaseUser,
        on_delete=models.CASCADE,
        help_text="The person who is associated with this work shift.",
    )
    start = models.DateTimeField(help_text="The time that the shift starts.")
    duration = models.DurationField(help_text="How long the shift will last, in HH:MM:SS format.")
    location = models.CharField(
        max_length=32,
        help_text="The location where the shift will be occur, e.g. GSMN 64.",
    )
    kind = models.CharField(
        max_length=8,
        choices=(("SI", "SI"), ("Tutoring", "Tutoring")),
        help_text="The kind of shift this is.",
    )

    def __str__(self):
        return f"{self.associated_person} in {self.location} at {self.start}"


class ShiftChangeRequest(models.Model):
    target = models.ForeignKey(
        to=Shift,
        related_name="shift_change_request_target",
        on_delete=models.CASCADE,
        help_text="Shift to edit.",
    )
    reason = models.CharField(
        max_length=512,
        help_text="Explanation for why this change is being requested.",
    )
    approved = models.BooleanField(
        default=False,
        help_text="Whether the request is approved or not.",
    )
    approved_by = models.ForeignKey(
        to=LRCDatabaseUser,
        related_name="shift_change_request_approved_by",
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        help_text="The user (if any) who approved the change request.",
    )
    approved_on = models.DateTimeField(
        help_text="When the request was approved.",
        blank=True,
        null=True,
        default=None,
    )

    new_associated_person = models.ForeignKey(
        to=LRCDatabaseUser,
        related_name="shift_change_request_new_associated_person",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        help_text="The new person who will be associated with this shift if this request is approved.",
    )
    new_start = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="The new time that the shift starts if this request is approved.",
    )
    new_duration = models.DurationField(
        blank=True,
        null=True,
        default=None,
        help_text="How long the shift will last, in HH:MM:SS format, if this request is approved.",
    )
    new_location = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        default=None,
        help_text="The new location where this shift will occur, e.g. GSMN 64, if this request is approved.",
    )


class Hardware(models.Model):
    class Meta:
        verbose_name_plural = "hardware"

    name = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Loan(models.Model):
    target = models.ForeignKey(
        to=Hardware,
        related_name="intended_hardware_to_borrow",
        on_delete=models.CASCADE,
        help_text="The desired hardware being requested",
    )

    hardware_user = models.ForeignKey(
        to=LRCDatabaseUser,
        on_delete=models.CASCADE,
        help_text="The LRC user borrowing the hardware",
    )

    start_time = models.DateTimeField()

    return_time = models.DateTimeField(null=True, blank=True)
