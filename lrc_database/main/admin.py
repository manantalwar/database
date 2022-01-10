from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Course, Hardware, LRCDatabaseUser, TutoringShift, TutoringShiftChangeRequest, Loan


class CourseAdmin(admin.ModelAdmin):
    ordering = ("department", "number")


class LRCDatabaseUserAdmin(UserAdmin):
    pass


class TutoringShiftAdmin(admin.ModelAdmin):
    list_display = ("tutor", "start", "duration", "location")


class TutoringShiftChangeRequestAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Approval",
            {"fields": ("target", "reason", "approved", "approved_by", "approved_on")},
        ),
        (
            "New data",
            {"fields": ("new_tutor", "new_start", "new_duration", "new_location")},
        ),
    )
    list_display = ("target", "reason", "approved", "approved_by", "approved_on")


class HardwareAdmin(admin.ModelAdmin):
    list_display = ("name", "is_available")
    ordering = ("name", "is_available")
    list_editable = ("is_available",)


class LoanAdmin(admin.ModelAdmin):
    list_display = ("target", "start_time", "return_time", "hardware_user")


admin.site.register(Course, CourseAdmin)
admin.site.register(LRCDatabaseUser, LRCDatabaseUserAdmin)
admin.site.register(TutoringShift, TutoringShiftAdmin)
admin.site.register(TutoringShiftChangeRequest, TutoringShiftChangeRequestAdmin)
admin.site.register(Hardware, HardwareAdmin)
admin.site.register(Loan, LoanAdmin)
