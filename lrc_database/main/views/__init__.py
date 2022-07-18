import json
import logging
from typing import Any, Callable, Concatenate, ParamSpec

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse

from ..forms import CourseForm, EditProfileForm, NewChangeRequestForm
from ..models import Course, Shift, ShiftChangeRequest

User = get_user_model()
log = logging.getLogger()


P = ParamSpec("P")


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


@login_required
def index(request):
    pending_shift_change_requests = ShiftChangeRequest.objects.filter(
        target__associated_person=request.user, approved=False
    )
    return render(request, "index.html", {"change_requests": pending_shift_change_requests})


@login_required
def user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_users_shifts = Shift.objects.filter(associated_person=target_user)
    target_users_shifts = [
        {
            "id": str(shift.id),
            "start": shift.start.isoformat(),
            "end": (shift.start + shift.duration).isoformat(),
            "title": str(shift),
            "allDay": False,
            "url": reverse("view_shift", args=(shift.id,)),
        }
        for shift in target_users_shifts
    ]
    target_users_shifts = json.dumps(target_users_shifts)
    return render(
        request, "users/user_profile.html", {"target_user": target_user, "target_users_shifts": target_users_shifts}
    )


@login_required
def edit_profile(request, user_id):
    if user_id != request.user.id:
        # TODO: let privileged users edit anyone's profile
        raise PermissionDenied
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            return HttpResponseRedirect(reverse("user_profile", args=(user_id,)))
    else:
        form = EditProfileForm(instance=user)
        return render(request, "users/edit_profile.html", {"user_id": user_id, "form": form})


@restrict_to_groups("Office staff", "Supervisors")
def list_users(request: HttpRequest, group: str) -> HttpResponse:
    users = get_list_or_404(User.objects.order_by("last_name"), groups__name=group)
    return render(request, "users/list_users.html", {"users": users, "group": group})


@login_required
def view_shift(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    change_requests = ShiftChangeRequest.objects.filter(target=shift)
    return render(request, "shifts/view_shift.html", {"shift": shift, "change_requests": change_requests})


@login_required
def new_shift_change_request(request, shift_id):
    shift = get_object_or_404(Shift, pk=shift_id)
    if shift.associated_person.id != request.user.id:
        # TODO: let privileged users edit anyone's shifts
        raise PermissionDenied
    if request.method == "POST":
        form = NewChangeRequestForm(request.POST)
        if form.is_valid():
            s = ShiftChangeRequest(
                target=shift, approved=False, approved_by=None, approved_on=None, **form.cleaned_data
            )
            s.save()
            return HttpResponseRedirect(reverse("view_shift", args=(shift_id,)))
    else:
        form = NewChangeRequestForm(
            initial={
                "new_associated_person": shift.associated_person,
                "new_start": shift.start,
                "new_duration": shift.duration,
                "new_location": shift.location,
            }
        )
        return render(request, "shifts/new_shift_change_request.html", {"shift_id": shift_id, "form": form})


@login_required
def list_courses(request):
    courses = Course.objects.order_by("department", "number")
    return render(request, "courses/list_courses.html", {"courses": courses})


@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    tutors = User.objects.filter(courses_tutored__in=(course,))
    sis = User.objects.filter(si_course=course)
    return render(request, "courses/view_course.html", {"course": course, "tutors": tutors, "sis": sis})


@restrict_to_groups("Office staff", "Supervisors")
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            c = Course(**form.cleaned_data)
            c.save()
            return HttpResponseRedirect(reverse("view_course", args=(c.id,)))
    else:
        form = CourseForm()
        return render(request, "courses/add_course.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course.department = form.cleaned_data["department"]
            course.number = form.cleaned_data["number"]
            course.name = form.cleaned_data["name"]
            course.save()
            return HttpResponseRedirect(reverse("view_course", args=(course.id,)))
    else:
        form = CourseForm(
            initial={
                "department": course.department,
                "number": course.number,
                "name": course.name,
            }
        )
        return render(request, "courses/edit_course.html", {"form": form, "course_id": course.id})


@restrict_to_groups("Office staff", "Supervisors")
def view_shift_change_requests(request, kind):
    requests = get_list_or_404(ShiftChangeRequest, target__kind=kind, approved=False)
    return render(request, "scheduling/view_shift_change_requests.html", {"change_requests": requests, "kind": kind})
