from typing import List, Union

from django.contrib.auth import views as auth_views
from django.urls import URLPattern, URLResolver, include, path

from .views import index
from .views.bulk_shift_editing_views import (
    drop_shifts_on_date,
    drop_shifts_on_date_confirmation,
    move_shifts_from_date,
    move_shifts_from_date_confirmation,
    swap_shift_dates,
    swap_shift_dates_confirmation,
)
from .views.courses import add_course, course_event_feed, edit_course, list_courses, view_course
from .views.hardware import add_hardware, add_loans, edit_hardware, edit_loans, show_hardware, show_loans
from .views.shifts import (
    approve_pending_request,
    deny_request,
    new_drop_request,
    new_shift,
    new_shift_change_request,
    new_shift_request,
    new_shift_tutors_only,
    view_shift,
    view_shift_change_request,
    view_shift_change_requests,
    view_shift_change_requests_by_user,
)
from .views.users import create_user, create_users_in_bulk, edit_profile, list_users, user_event_feed, user_profile

URLs = List[Union[URLPattern, URLResolver]]

MISC_URLS: URLs = [
    path("", index, name="index"),
]

ACCOUNTS_URLS: URLs = [
    # path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/password_change/", auth_views.PasswordChangeView.as_view(), name="password_change"),
    path("accounts/password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
]

API_URLS: URLs = [
    path("api/course_event_feed/<int:course_id>", course_event_feed, name="course_event_feed"),
    path("api/user_event_feed/<int:user_id>", user_event_feed, name="user_event_feed"),
]

COURSES_URLS: URLs = [
    path("courses/", list_courses, name="list_courses"),
    path("courses/<int:course_id>", view_course, name="view_course"),
    path("courses/<int:course_id>/edit", edit_course, name="edit_course"),
    path("courses/add", add_course, name="add_course"),
]

HARDWARE_URLS: URLs = [
    path("show_hardware", show_hardware, name="showHardware"),
    path("show_loans", show_loans, name="showLoans"),
    path("edit_loans/<int:loan_id>", edit_loans, name="edit_loans"),
    path("edit_hardware/<int:hardware_id>", edit_hardware, name="edit_hardware"),
    path("add_hardware", add_hardware, name="add_hardware"),
    path("add_loans", add_loans, name="add_loans"),
]

SCHEDULING_URLS: URLs = [
    # fmt: off
    path("scheduling/bulk/drop_on_date", drop_shifts_on_date, name="drop_shifts_on_date"),
    path("scheduling/bulk/drop_on_date/confirm", drop_shifts_on_date_confirmation, name="drop_shifts_on_date_confirmation"),
    path("scheduling/bulk/swap_shift_dates", swap_shift_dates, name="swap_shift_dates"),
    path("scheduling/bulk/swap_shift_dates/confirmation", swap_shift_dates_confirmation, name="swap_shift_dates_confirmation"),
    path("scheduling/bulk/move_shifts_from_date", move_shifts_from_date, name="move_shifts_from_date"),
    path("scheduling/bulk/move_shifts_from_date/confirm", move_shifts_from_date_confirmation, name="move_shifts_from_date_confirmation"),
    path("scheduling/shift_change_requests/<int:request_id>", view_shift_change_request, name="view_single_request"),
    path("scheduling/shift_change_requests/<int:request_id>/deny", deny_request, name="deny_request"),
    path("scheduling/shift_change_requests/<int:request_id>/approval_form", approve_pending_request, name="approve_request"),
    path("scheduling/shift_change_requests/<str:kind>/<str:state>", view_shift_change_requests, name="view_shift_change_requests"),
    path("scheduling/request_shift", new_shift_request, name="new_shift_request"),
    # fmt: on
]

SHIFTS_URLS: URLs = [
    path("shifts/<int:shift_id>", view_shift, name="view_shift"),
    path("shifts/<int:shift_id>/request_drop", new_drop_request, name="new_drop_request"),
    path("shifts/<int:shift_id>/request_change", new_shift_change_request, name="new_shift_change_request"),
    path("shifts/new", new_shift, name="new_shift"),
    path("shifts/new/tutoring", new_shift_tutors_only, name="new_shift_tutors_only"),
]

USERS_URLS: URLs = [
    path("users/", list_users, name="list_users"),
    path("users/<int:user_id>", user_profile, name="user_profile"),
    path("users/<int:user_id>/edit", edit_profile, name="edit_profile"),
    path(
        "users/<int:user_id>/shift_change_requests",
        view_shift_change_requests_by_user,
        name="view_shift_change_requests_by_user",
    ),
    path("users/create", create_user, name="create_user"),
    path("users/create/bulk", create_users_in_bulk, name="create_users_in_bulk"),
    path("users/groups/<str:group>", list_users, name="list_users"),
]

urlpatterns: URLs = (
    MISC_URLS + ACCOUNTS_URLS + API_URLS + COURSES_URLS + HARDWARE_URLS + SCHEDULING_URLS + SHIFTS_URLS + USERS_URLS
)
