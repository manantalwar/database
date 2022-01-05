from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Course, LRCDatabaseUser, TutoringShift, TutoringShiftChangeRequest


class CourseAdmin(admin.ModelAdmin):
    pass


class LRCDatabaseUserAdmin(UserAdmin):
    pass


class TutoringShiftAdmin(admin.ModelAdmin):
    pass


class TutoringShiftChangeRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(LRCDatabaseUser, LRCDatabaseUserAdmin)
admin.site.register(TutoringShift, TutoringShiftAdmin)
admin.site.register(TutoringShiftChangeRequest, TutoringShiftChangeRequestAdmin)
