from typing import Callable, Concatenate, ParamSpec

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from ..models import SIShiftChangeRequest, TutorShiftChangeRequest

P = ParamSpec("P")
User = get_user_model()


def restrict_to_groups(
    *groups: str,
) -> Callable[
    [Callable[Concatenate[HttpRequest, P], HttpResponse]], Callable[Concatenate[HttpRequest, P], HttpResponse]
]:
    def decorator(
        view: Callable[Concatenate[HttpRequest, P], HttpResponse]
    ) -> Callable[Concatenate[HttpRequest, P], HttpResponse]:
        def _wrapped_view(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> HttpResponse:
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or request.user.groups.filter(name__in=groups).exists():
                return view(request, *args, **kwargs)
            raise PermissionDenied

        return _wrapped_view

    return decorator


def restrict_to_http_methods(
    *methods: str,
) -> Callable[
    [Callable[Concatenate[HttpRequest, P], HttpResponse]], Callable[Concatenate[HttpRequest, P], HttpResponse]
]:
    """
    Annotation for views that only work with one HTTP method. If a request is made for the view with an acceptable
    method, is goes through like normal. If a request is made with an unacceptable method, an HTTP 405 (Method Not
    Allowed) is returned instead with a header specifying the allowed methods.
    """

    def decorator(
        view: Callable[Concatenate[HttpRequest, P], HttpResponse]
    ) -> Callable[Concatenate[HttpRequest, P], HttpResponse]:
        def _wrapped_view(request: HttpRequest, *args: P.args, **kwargs: P.kwargs):
            if request.method in methods:
                return view(request, *args, **kwargs)
            else:
                return HttpResponseNotAllowed(methods)

        return _wrapped_view

    return decorator


def personal(
    view: Callable[Concatenate[HttpRequest, int, P], HttpResponse]
) -> Callable[Concatenate[HttpRequest, int, P], HttpResponse]:
    """
    Annotation for views that are "personal" to some user, meaning they should only be viewable to that user and
    privileged users.
    """

    def _wrapped_view(request: HttpRequest, user_id: int, *args: P.args, **kwargs: P.kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        if request.user.id == user_id or request.user.is_privileged():
            return view(request, user_id, *args, **kwargs)
        raise PermissionDenied

    return _wrapped_view


@login_required
def index(request):
    if request.user.groups.filter(name__in=("Tutors", "SIs")).exists():
        return redirect("user_profile", request.user.id)

    pending_si_shift_change_requests = SIShiftChangeRequest.objects.filter(
        target__associated_person=request.user, request_state="New"
    )
    pending_tutor_shift_change_requests = TutorShiftChangeRequest.objects.filter(
        target__associated_person=request.user, request_state="New"
    )

    return render(
        request,
        "index.html",
        {
            "si_change_requests": pending_si_shift_change_requests,
            "tutor_change_request": pending_tutor_shift_change_requests,
        },
    )
