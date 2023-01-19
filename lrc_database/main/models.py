import datetime

import pytz
from django import forms
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models
from django.db.models.query import QuerySet


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

    def is_privileged(self) -> bool:
        return self.groups.filter(name__in=("Office staff", "Supervisors")).exists()

    def __str__(self) -> str:
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
        help_text="The kind of shift this is: tutoring or SI.",
    )

    @staticmethod
    def all_on_date(date: datetime.date) -> QuerySet["Shift"]:
        tz_adjusted_range_start = datetime.datetime(
            date.year, date.month, date.day, tzinfo=pytz.timezone("America/New_York")
        )
        tz_adjusted_range_end = tz_adjusted_range_start + datetime.timedelta(days=1)
        return Shift.objects.filter(
            start__gte=tz_adjusted_range_start,
            start__lte=tz_adjusted_range_end,
        )

    def __str__(self):
        tz = pytz.timezone("America/New_York")
        return f"{self.associated_person} in {self.location} at {self.start.astimezone(tz)}"


class ShiftChangeRequest(models.Model):
    shift_to_update = models.ForeignKey(
        to=Shift,
        related_name="shift_change_request_target",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        help_text="Shift to edit. If none, this change request will create a new shift when approved.",
    )

    reason = models.CharField(
        max_length=512,
        help_text="Explanation for why this new shift or shift change is being requested.",
    )

    state = models.CharField(
        max_length=40,
        choices=(("Approved", "Approved"), ("Pending", "Pending"), ("Not Approved", "Not Approved"), ("New", "New")),
        help_text="The kind of shift this is.",
    )

    is_drop_request = models.BooleanField(default=False)

    new_associated_person = models.ForeignKey(
        to=LRCDatabaseUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        help_text="The person who is associated with this work shift.",
    )

    new_start = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="The date time that the shift starts if this request is approved.",
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
        help_text="The location where this shift will occur, e.g. GSMN 64, if this request is approved.",
    )

    new_kind = models.CharField(
        max_length=8,
        choices=(("SI", "SI"), ("Tutoring", "Tutoring")),
        blank=True,
        null=True,
        default=None,
        help_text="The kind of shift this is: tutoring or SI.",
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
        help_text="REQUESTED HARDWARE",
    )

    hardware_user = models.ForeignKey(
        to=LRCDatabaseUser,
        on_delete=models.CASCADE,
        help_text="LRC USER",
    )

    start_time = models.DateTimeField(
        help_text="DD/MM/YYYY HH:MM",
    )

    return_time = models.DateTimeField(
        blank=True,
        null=True,
        default=None,
        help_text="DD/MM/YYYY HH:MM",
    )
