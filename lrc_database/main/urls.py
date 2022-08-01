from django.urls import include, path

from .views import index
from .views.bulk_shift_editing_views import (
    drop_shifts_on_date,
    drop_shifts_on_date_confirmation,
    move_shifts_from_date,
    move_shifts_from_date_confirmation,
    swap_shift_dates,
    swap_shift_dates_confirmation,
)
from .views.courses import add_course, edit_course, list_courses, view_course
from .views.hardware import add_hardware, add_loans, edit_hardware, edit_loans, show_hardware, show_loans
from .views.shifts import (
    new_shift_change_request,
    view_approved_shift_change_requests,
    view_denied_shift_change_requests,
    view_pending_shift_change_requests,
    view_shift,
    view_shift_change_requests,
    view_single_request,
)
from .views.users import create_user, create_users_in_bulk, edit_profile, list_users, user_event_feed, user_profile

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("api/user_event_feed/<int:user_id>", user_event_feed, name="user_event_feed"),
    path("courses/", list_courses, name="list_courses"),
    path("courses/<int:course_id>", view_course, name="view_course"),
    path("courses/<int:course_id>/edit", edit_course, name="edit_course"),
    path("courses/add", add_course, name="add_course"),
    # view all new requests of a certain kind
    path(
        "scheduling/shift_change_requests/<str:kind>",
        view_shift_change_requests,
        name="view_shift_change_requests",
    ),
    # view all approved requests of a certain kind
    path(
        "scheduling/approved_shift_change_requests/<str:kind>",
        view_approved_shift_change_requests,
        name="view_approved_shift_change_requests",
    ),
    # view all denied requests of a certain kind
    path(
        "scheduling/denied_shift_change_requests/<str:kind>",
        view_denied_shift_change_requests,
        name="view_denied_shift_change_requests",
    ),
    # view all pending requests of a certain kind (just for SI)
    path(
        "scheduling/pending_shift_change_requests/<str:kind>",
        view_pending_shift_change_requests,
        name="view_pending_shift_change_requests",
    ),
    # view single request
    path(
        "scheduling/shift_change_requests/<str:kind>/<int:request_id>",
        view_single_request,
        name="view_single_si_request",
    ),
    path("scheduling/bulk/drop_on_date", drop_shifts_on_date, name="drop_shifts_on_date"),
    path(
        "scheduling/bulk/drop_on_date/confirm",
        drop_shifts_on_date_confirmation,
        name="drop_shifts_on_date_confirmation",
    ),
    path("scheduling/bulk/swap_shift_dates", swap_shift_dates, name="swap_shift_dates"),
    path(
        "scheduling/bulk/swap_shift_dates/confirmation",
        swap_shift_dates_confirmation,
        name="swap_shift_dates_confirmation",
    ),
    path("scheduling/move_shifts_from_date", move_shifts_from_date, name="move_shifts_from_date"),
    path(
        "scheduling/move_shifts_from_date/confirm",
        move_shifts_from_date_confirmation,
        name="move_shifts_from_date_confirmation",
    ),
    path("shifts/<int:shift_id>", view_shift, name="view_shift"),
    path("shifts/<int:shift_id>/request_change", new_shift_change_request, name="new_shift_change_request"),
    path("users/create", create_user, name="create_user"),
    path("users/create/bulk", create_users_in_bulk, name="create_users_in_bulk"),
    path("users/<int:user_id>", user_profile, name="user_profile"),
    path("users/<int:user_id>/edit", edit_profile, name="edit_profile"),
    path("users/<str:group>", list_users, name="list_users"),
    path("show_hardware", show_hardware, name="showHardware"),
    path("show_loans", show_loans, name="showLoans"),
    path("edit_loans/<int:loan_id>", edit_loans, name="edit_loans"),
    path("edit_hardware/<int:hardware_id>", edit_hardware, name="edit_hardware"),
    path("add_hardware", add_hardware, name="add_hardware"),
    path("add_loans", add_loans, name="add_loans"),
    path("users/groups/<str:group>", list_users, name="list_users"),
]
