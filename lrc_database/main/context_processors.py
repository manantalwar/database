from typing import TypedDict, Union

from django.db.models import Q
from django.http.request import HttpRequest

from .models import ShiftChangeRequest
from .templatetags.groups import is_privileged


class AlertCountDict(TypedDict):
    pending_si_change_count: int
    pending_tutoring_change_count: int
    total_alert_count: int


class EmptyDict(TypedDict):
    pass


def alert_counts(request: HttpRequest) -> Union[AlertCountDict, EmptyDict]:
    """
    Makes counts for various alert types available to all templates as variables, so that we can show alert counts in
    the navbar.
    """

    # If user is not signed in, do no queries.
    if not request.user.is_authenticated:
        return {}

    # If user doesn't have permission to manage shift change requests, do no queries.
    if not is_privileged(request.user):
        return {}

    si_count = ShiftChangeRequest.objects.filter(
        (Q(new_kind="SI") | Q(shift_to_update__kind="SI")), state="New"
    ).count()

    tutoring_count = ShiftChangeRequest.objects.filter(
        (Q(new_kind="Tutoring") | Q(shift_to_update__kind="Tutoring")), state="New"
    ).count()

    return {
        "pending_si_change_count": si_count,
        "pending_tutoring_change_count": tutoring_count,
        "total_alert_count": si_count + tutoring_count,
    }
