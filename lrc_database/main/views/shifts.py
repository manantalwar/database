from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render

from ..forms import NewSIChangeRequestForm, NewTutorChangeRequestForm
from ..models import Shift, SIShiftChangeRequest, TutorShiftChangeRequest
from . import restrict_to_groups, restrict_to_http_methods


@login_required
@restrict_to_http_methods("GET")
def view_shift(request: HttpRequest, shift_id: int) -> HttpResponse:
    shift = get_object_or_404(Shift, pk=shift_id)
    if shift.kind == "SI":
        change_requests = SIShiftChangeRequest.objects.filter(target=shift)
        return render(
            request,
            "shifts/view_shift.html",
            {"shift": shift, "change_requests": change_requests},
        )
    else:
        change_requests2 = TutorShiftChangeRequest.objects.filter(target=shift)
        return render(
            request,
            "shifts/view_shift.html",
            {"shift": shift, "change_requests": change_requests2},
        )


@login_required
@restrict_to_http_methods("GET", "POST")
def new_shift_change_request(request: HttpRequest, shift_id: int) -> HttpResponse:
    shift = get_object_or_404(Shift, pk=shift_id)
    if shift.associated_person.id != request.user.id:
        # TODO: let privileged users edit anyone's shifts
        raise PermissionDenied
    if shift.kind == "SI":
        if request.method == "POST":
            form = NewSIChangeRequestForm(request.POST)
            if form.is_valid():
                s = SIShiftChangeRequest(
                    target=shift, request_state="New", approved_by=None, approved_on=None, **form.cleaned_data
                )
                s.save()
                return redirect("view_shift", shift_id)
            else:
                messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
                return redirect("new_shift_change_request", shift_id)
        else:
            form = NewSIChangeRequestForm(
                initial={
                    "new_start": shift.start,
                    "new_duration": shift.duration,
                    "new_location": shift.location,
                }
            )
        return render(
            request,
            "shifts/new_shift_change_request.html",
            {"shift_id": shift_id, "form": form},
        )
    else:
        if request.method == "POST":
            form2 = NewTutorChangeRequestForm(request.POST)
            if form.is_valid():
                s2 = TutorShiftChangeRequest(
                    target=shift, request_state="New", approved_by=None, approved_on=None, **form.cleaned_data
                )
                s2.save()
                return redirect("view_shift", shift_id)
            else:
                messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
                return redirect("new_shift_change_request", shift_id)
        else:
            form2 = NewTutorChangeRequestForm(
                initial={
                    "new_associated_person": shift.associated_person,
                    "new_start": shift.start,
                    "new_duration": shift.duration,
                    "new_location": shift.location,
                }
            )
        return render(
            request,
            "shifts/new_shift_change_request.html",
            {"shift_id": shift_id, "form": form},
        )


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def view_shift_change_requests(request: HttpRequest, kind: str) -> HttpResponse:
    if kind == "Tutor":
        requests = get_list_or_404(TutorShiftChangeRequest, target__kind=kind, request_state="New")
        return render(
            request,
            "scheduling/view_shift_change_requests.html",
            {"change_requests": requests, "kind": kind},
        )
    else:
        requests2 = get_list_or_404(SIShiftChangeRequest, target__kind=kind, request_state="New")
        return render(
            request,
            "scheduling/view_shift_change_requests.html",
            {"change_requests": requests2, "kind": kind},
        )


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def view_single_request(request: HttpRequest, kind: str, request_id: int) -> HttpResponse:
    if kind == "SI":
        shift_request = get_object_or_404(SIShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_request.html", {"shift_request": shift_request, "kind": kind})
    else:
        shift_request2 = get_object_or_404(TutorShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_request.html", {"shift_request": shift_request2, "kind": kind})
