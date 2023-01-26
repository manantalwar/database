from typing import TypedDict, Union

from django.db.models import Q
from django.http.request import HttpRequest

from .models import ShiftChangeRequest
from .templatetags.groups import is_privileged


class AlertCountDict(TypedDict):
    pending_si_change_count: int
    pending_tutoring_change_count: int
    pending_si_drop_count: int
    pending_tutoring_drop_count: int
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
    )
    si_count_change = si_count.filter(is_drop_request=False).count()
    si_count_drop = si_count.filter(is_drop_request=True).count()
    
    tutoring_count = ShiftChangeRequest.objects.filter(
        (Q(new_kind="Tutoring") | Q(shift_to_update__kind="Tutoring")), state="New"
    )
    tutoring_count_change = tutoring_count.filter(is_drop_request=False).count()
    tutoring_count_drop = tutoring_count.filter(is_drop_request=True).count()

    total = si_count_change + si_count_drop + tutoring_count_change + tutoring_count_drop

    return {
        "pending_si_change_count": si_count_change,
        "pending_tutoring_change_count": tutoring_count_change,
        "pending_si_drop_count": si_count_drop,
        "pending_tutoring_drop_count": tutoring_count_drop,
        "total_alert_count": total,
    }
