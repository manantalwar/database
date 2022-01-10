from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Course, Hardware, LRCDatabaseUser, TutoringShift, TutoringShiftChangeRequest


class CourseAdmin(admin.ModelAdmin):
    pass


class LRCDatabaseUserAdmin(UserAdmin):
    pass


class TutoringShiftAdmin(admin.ModelAdmin):
    pass


class TutoringShiftChangeRequestAdmin(admin.ModelAdmin):
    pass


class HardwareAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(LRCDatabaseUser, LRCDatabaseUserAdmin)
admin.site.register(TutoringShift, TutoringShiftAdmin)
admin.site.register(TutoringShiftChangeRequest, TutoringShiftChangeRequestAdmin)
admin.site.register(Hardware, HardwareAdmin)
