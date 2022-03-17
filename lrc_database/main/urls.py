from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("courses/", views.list_courses, name="list_courses"),
    path("courses/<int:course_id>", views.view_course, name="view_course"),
    path(
        "scheduling/shift_change_requests/<str:kind>",
        views.view_shift_change_requests,
        name="view_shift_change_requests",
    ),
    path("shifts/<int:shift_id>", views.view_shift, name="view_shift"),
    path("shifts/<int:shift_id>/request_change", views.new_shift_change_request, name="new_shift_change_request"),
    path("users/<int:user_id>", views.user_profile, name="user_profile"),
    path("users/<int:user_id>/edit", views.edit_profile, name="edit_profile"),
    path("users/<str:group>", views.list_users, name="list_users"),
]
