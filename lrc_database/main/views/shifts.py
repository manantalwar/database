from datetime import datetime, timedelta
from typing import Optional

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from ..forms import (
    ApproveChangeRequestForm,
    NewChangeRequestForm,
    NewDropRequestForm,
    NewShiftForm,
    NewShiftForTutorForm,
)
from ..models import Shift, ShiftChangeRequest
from ..templatetags.groups import is_privileged
from . import restrict_to_groups, restrict_to_http_methods


@login_required
@restrict_to_http_methods("GET")
def view_shift(request: HttpRequest, shift_id: int) -> HttpResponse:
    shift = get_object_or_404(Shift, pk=shift_id)
    change_requests = ShiftChangeRequest.objects.filter(shift_to_update=shift)
    return render(
        request,
        "shifts/view_shift.html",
        {"shift": shift, "change_requests": change_requests},
    )


@login_required
@restrict_to_http_methods("GET", "POST")
def new_shift_change_request(request: HttpRequest, shift_id: int) -> HttpResponse:
    shift = get_object_or_404(Shift, pk=shift_id)
    if shift.associated_person.id != request.user.id:
        # TODO: let privileged users edit anyone's shifts
        raise PermissionDenied
    if request.method == "POST":
        form = NewChangeRequestForm(request.POST)
        if form.is_valid():
            s = ShiftChangeRequest(
                shift_to_update=shift,
                state="New",
                new_associated_person=request.user,
                # approved_by=None,
                # approved_on=None,
                **form.cleaned_data,
            )
            s.save()
            return redirect("view_shift", shift_id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("new_shift_change_request", shift_id)
    else:
        form = NewChangeRequestForm(
            initial={
                "new_start": shift.start,
                "new_duration": shift.duration,
                "new_location": shift.location,
                "new_kind": shift.kind,
            }
        )
        return render(
            request,
            "shifts/new_shift_change_request.html",
            {"shift_id": shift_id, "form": form},
        )


# View all NEW requests
@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def view_shift_change_requests(request: HttpRequest, kind: str, state: str) -> HttpResponse:
    requests = ShiftChangeRequest.objects.filter((Q(new_kind=kind) | Q(shift_to_update__kind=kind)), state=state)
    return render(
        request,
        "scheduling/view_shift_change_requests.html",
        {"change_requests": requests, "kind": kind, "state": state},
    )


@login_required
@restrict_to_http_methods("GET")
def view_shift_change_requests_by_user(request: HttpRequest, user_id: int) -> HttpResponse:
    if not is_privileged(request.user) and request.user.id != user_id:
        raise PermissionDenied
    requests = ShiftChangeRequest.objects.filter(
        (Q(new_associated_person__id=user_id) | Q(shift_to_update__associated_person__id=user_id)),
    )
    return render(
        request,
        "scheduling/view_shift_change_requests.html",
        {"change_requests": requests, "kind": f"User #{user_id}'s"},
    )


@restrict_to_http_methods("GET")
def view_shift_change_request(request: HttpRequest, request_id: int) -> HttpResponse:
    shift_request = get_object_or_404(ShiftChangeRequest, pk=request_id)
    is_for_user = False
    if shift_request.new_associated_person == request.user:
        is_for_user = True
    elif shift_request.shift_to_update is not None and shift_request.shift_to_update.associated_person == request.user:
        is_for_user = True
    if not is_privileged(request.user) and not is_for_user:
        raise PermissionDenied
    return render(request, "shifts/view_request.html", {"shift_request": shift_request})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def deny_request(request: HttpRequest, request_id: int) -> HttpResponse:
    shift_request = get_object_or_404(ShiftChangeRequest, id=request_id)
    shift_request.state = "Not Approved"
    shift_request.save()
    return redirect("view_single_request", request_id)


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def approve_pending_request(request: HttpRequest, request_id: int) -> HttpResponse:
    request_cur = get_object_or_404(ShiftChangeRequest, id=request_id)
    shift = request_cur.shift_to_update or Shift()

    if request_cur.is_drop_request:
        request_cur.shift_to_update.delete()
        messages.add_message(request, messages.INFO, "Shift dropped.")
        return redirect("index")

    initial = {
        "associated_person": request_cur.new_associated_person or shift.associated_person,
        "start": request_cur.new_start or shift.start,
        "duration": request_cur.new_duration or shift.duration,
        "location": request_cur.new_location or shift.location,
        "kind": request_cur.new_kind or shift.kind,
    }

    if request.method == "POST":
        form = ApproveChangeRequestForm(
            request.POST,
            instance=shift,
            initial=initial,
        )

        if not form.is_valid():
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("view_single_request", request_id)

        form.save()
        request_cur.state = "Approved"
        request_cur.save()
        return redirect("index")

    else:
        form = ApproveChangeRequestForm(instance=shift, initial=initial)
        return render(request, "scheduling/approvePendingForm.html", {"form": form, "request_id": request_id})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def new_shift(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = NewShiftForm()
        return render(request, "shifts/new_shift.html", {"form": form})
    else:
        form = NewShiftForm(request.POST)
        if form.is_valid():
            shift = Shift(**form.cleaned_data)
            shift.save()
            return redirect("view_shift", shift.id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("new_shift")


@restrict_to_groups("Tutors")
@restrict_to_http_methods("GET", "POST")
def new_shift_tutors_only(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = NewShiftForTutorForm()
        return render(
            request,
            "generic_form.html",
            {"form": form, "form_action_url": reverse("new_shift_tutors_only"), "form_title": "Create new shift"},
        )
    else:
        form = NewShiftForTutorForm(request.POST)
        if form.is_valid():
            shift = Shift(associated_person=request.user, location="LRC", kind="Tutoring", **form.cleaned_data)
            shift.save()
            return redirect("view_shift", shift.id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("new_shift_tutors_only")


@restrict_to_groups("SIs")
@restrict_to_http_methods("GET", "POST")
def new_shift_request(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = NewChangeRequestForm()
        return render(
            request,
            "shifts/new_shift_request.html",
            {"form": form},
        )
    else:
        form = NewChangeRequestForm(request.POST)
        print(form.data)
        if form.is_valid():
            change_request = ShiftChangeRequest(
                shift_to_update=None,
                state="New",
                new_associated_person=request.user,
                # approved_by=None,
                # approved_on=None,
                **form.cleaned_data,
            )
            change_request.save()
            return redirect("view_single_request", change_request.id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("new_shift_request")


@restrict_to_groups("SIs")
@restrict_to_http_methods("GET", "POST")
def new_drop_request(request: HttpRequest, shift_id: int) -> HttpResponse:
    shift = get_object_or_404(Shift, id=shift_id)
    if shift.associated_person != request.user:
        print(shift.associated_person)
        print(request.user)
        raise PermissionDenied

    if request.method == "GET":
        form = NewDropRequestForm()
        return render(
            request,
            "shifts/new_drop_request.html",
            {"form": form, "shift_id": shift_id},
        )
    else:
        form = NewDropRequestForm(request.POST)
        if form.is_valid():
            change_request = ShiftChangeRequest(
                shift_to_update=shift,
                state="New",
                is_drop_request=True,
                # approved_by=None,
                # approved_on=None,
                **form.cleaned_data,
            )
            change_request.save()
            return redirect("view_single_request", change_request.id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("new_shift_request")
