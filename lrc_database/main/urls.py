from django.urls import include, path

from . import views
from .views.bulk_shift_editing_views import drop_shifts_on_date, drop_shifts_on_date_confirmation

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("courses/", views.list_courses, name="list_courses"),
    path("courses/<int:course_id>", views.view_course, name="view_course"),
    path("courses/<int:course_id>/edit", views.edit_course, name="edit_course"),
    path("courses/add", views.add_course, name="add_course"),
    path(
        "scheduling/shift_change_requests/<str:kind>",
        views.view_shift_change_requests,
        name="view_shift_change_requests",
    ),
    path("scheduling/bulk/drop_on_date", drop_shifts_on_date, name="drop_shifts_on_date"),
    path(
        "scheduling/bulk/drop_on_date/confirm",
        drop_shifts_on_date_confirmation,
        name="drop_shifts_on_date_confirmation",
    ),
    path("shifts/<int:shift_id>", views.view_shift, name="view_shift"),
    path("shifts/<int:shift_id>/request_change", views.new_shift_change_request, name="new_shift_change_request"),
    path("users/<int:user_id>", views.user_profile, name="user_profile"),
    path("users/<int:user_id>/edit", views.edit_profile, name="edit_profile"),
    path("users/<str:group>", views.list_users, name="list_users"),
]
