from typing import TypedDict, Union

from django.http.request import HttpRequest

from .models import ShiftChangeRequest


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

    if not request.user.is_authenticated:
        return {}
    if not request.user.groups.filter(name__in=("Office staff", "Supervisors")).exists():
        return {}
    si_count = ShiftChangeRequest.objects.filter(target__kind="SI").count()
    tutoring_count = ShiftChangeRequest.objects.filter(target__kind="Tutoring").count()
    return {
        "pending_si_change_count": si_count,
        "pending_tutoring_change_count": tutoring_count,
        "total_alert_count": si_count + tutoring_count,
    }
