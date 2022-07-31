from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Course, Hardware, Loan, LRCDatabaseUser, Shift, SIShiftChangeRequest, TutorShiftChangeRequest


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    ordering = ("department", "number")


@admin.register(LRCDatabaseUser)
class LRCDatabaseUserAdmin(UserAdmin):
    pass


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = (
        "associated_person",
        "start",
        "duration",
        "location",
    )


@admin.register(SIShiftChangeRequest)
class SIShiftChangeRequestAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Approval",
            {
                "fields": (
                    "target",
                    "reason",
                    "request_state",
                    "approved_by",
                    "approved_on",
                )
            },
        ),
        (
            "New data",
            {
                "fields": (
                    "new_start",
                    "new_duration",
                    "new_location",
                )
            },
        ),
    )
    list_display = (
        "target",
        "reason",
        "request_state",
        "approved_by",
        "approved_on",
    )


@admin.register(TutorShiftChangeRequest)
class TutorShiftChangeRequestAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Approval",
            {
                "fields": (
                    "target",
                    "reason",
                    "request_state",
                    "approved_by",
                    "approved_on",
                )
            },
        ),
        (
            "New data",
            {
                "fields": (
                    "new_associated_person",
                    "new_start",
                    "new_duration",
                    "new_location",
                )
            },
        ),
    )
    list_display = (
        "target",
        "reason",
        "request_state",
        "approved_by",
        "approved_on",
    )


@admin.register(Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ("name", "is_available")
    ordering = ("name", "is_available")
    list_editable = ("is_available",)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "target",
        "start_time",
        "return_time",
        "hardware_user",
    )
