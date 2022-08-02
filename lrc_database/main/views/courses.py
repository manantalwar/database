from datetime import datetime
from typing import Any, Dict

from django.core.exceptions import BadRequest
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..forms import CourseForm
from ..models import Course, Shift
from . import restrict_to_groups, restrict_to_http_methods

User = get_user_model()


@login_required
@restrict_to_http_methods("GET")
def list_courses(request: HttpRequest) -> HttpResponse:
    courses = Course.objects.order_by("department", "number")
    return render(request, "courses/list_courses.html", {"courses": courses})


@login_required
@restrict_to_http_methods("GET")
def view_course(request: HttpRequest, course_id: int) -> HttpResponse:
    course = get_object_or_404(Course, id=course_id)
    tutors = User.objects.filter(courses_tutored__in=(course,))
    sis = User.objects.filter(si_course=course)
    return render(
        request,
        "courses/view_course.html",
        {"course": course, "tutors": tutors, "sis": sis},
    )


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def add_course(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            c = Course(**form.cleaned_data)
            c.save()
            return redirect("view_course", c.id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("add_course")
    else:
        form = CourseForm()
        return render(request, "courses/add_course.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def edit_course(request: HttpRequest, course_id: int) -> HttpResponse:
    course = get_object_or_404(Course, pk=course_id)
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course.department = form.cleaned_data["department"]
            course.number = form.cleaned_data["number"]
            course.name = form.cleaned_data["name"]
            course.save()
            return redirect("view_course", course.id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("edit_course", course_id)
    else:
        form = CourseForm(
            initial={
                "department": course.department,
                "number": course.number,
                "name": course.name,
            }
        )
        return render(request, "courses/edit_course.html", {"form": form, "course_id": course.id})


@login_required
@restrict_to_http_methods("GET")
def course_event_feed(request: HttpRequest, course_id: int) -> JsonResponse:
    try:
        start = datetime.fromisoformat(request.GET["start"])
        end = datetime.fromisoformat(request.GET["end"])
    except KeyError:
        raise BadRequest("Both start and end dates must be specified.")
    except ValueError:
        raise BadRequest("Either start or end date is not in correct ISO8601 format.")

    course = get_object_or_404(Course, id=course_id)

    # TODO: problematic, see comment on user_event_feed
    shifts = Shift.objects.filter(
        Q(associated_person__si_course=course) | Q(associated_person__courses_tutored=course),
        start__gte=start,
        start__lte=end
    )

    def to_json(shift: Shift) -> Dict[str, Any]:
        return {
            "id": str(shift.id),
            "start": shift.start.isoformat(),
            "end": (shift.start + shift.duration).isoformat(),
            "title": str(shift),
            "allDay": False,
            "url": reverse("view_shift", args=(shift.id,)),
        }

    json_response = list(map(to_json, shifts))
    return JsonResponse(json_response, safe=False)