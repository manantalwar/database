from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render

from ..forms import NewSIChangeRequestForm, NewTutorChangeRequestForm, SIApproveRequestForm
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


# View all NEW requests
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


# View all APPROVED requests
@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def view_approved_shift_change_requests(request: HttpRequest, kind: str) -> HttpResponse:
    if kind == "Tutor":
        requests = get_list_or_404(TutorShiftChangeRequest, target__kind=kind, request_state="Approved")
        return render(
            request,
            "scheduling/view_approved_shift_change_requests.html",
            {"change_requests": requests, "kind": kind},
        )
    else:
        requests2 = get_list_or_404(SIShiftChangeRequest, target__kind=kind, request_state="Approved")
        return render(
            request,
            "scheduling/view_approved_shift_change_requests.html",
            {"change_requests": requests2, "kind": kind},
        )


# view all DENIED requests
@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def view_denied_shift_change_requests(request: HttpRequest, kind: str) -> HttpResponse:
    if kind == "Tutor":
        requests = get_list_or_404(TutorShiftChangeRequest, target__kind=kind, request_state="Not Approved")
        return render(
            request,
            "scheduling/view_denied_shift_change_requests.html",
            {"change_requests": requests, "kind": kind},
        )
    else:
        requests2 = get_list_or_404(SIShiftChangeRequest, target__kind=kind, request_state="Not Approved")
        return render(
            request,
            "scheduling/view_denied_shift_change_requests.html",
            {"change_requests": requests2, "kind": kind},
        )


# View all PENDING requests
@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def view_pending_shift_change_requests(request: HttpRequest, kind: str) -> HttpResponse:
    if kind == "Tutor":
        return redirect(view_shift_change_requests, kind)
    else:
        requests2 = get_list_or_404(SIShiftChangeRequest, target__kind=kind, request_state="Pending")
        return render(
            request,
            "scheduling/view_pending_shift_change_requests.html",
            {"change_requests": requests2, "kind": kind},
        )


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
# View new requests
def view_single_request(request: HttpRequest, kind: str, request_id: int) -> HttpResponse:
    if kind == "SI":
        shift_request = get_object_or_404(SIShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_request.html", {"shift_request": shift_request, "kind": kind})
    else:
        shift_request2 = get_object_or_404(TutorShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_request.html", {"shift_request": shift_request2, "kind": kind})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
# View approved requests
def view_approved_single_request(request: HttpRequest, kind: str, request_id: int) -> HttpResponse:
    if kind == "SI":
        shift_request = get_object_or_404(SIShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_approved_request.html", {"shift_request": shift_request, "kind": kind})
    else:
        shift_request2 = get_object_or_404(TutorShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_approved_request.html", {"shift_request": shift_request2, "kind": kind})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
# View denied requests
def view_denied_single_request(request: HttpRequest, kind: str, request_id: int) -> HttpResponse:
    if kind == "SI":
        shift_request = get_object_or_404(SIShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_denied_request.html", {"shift_request": shift_request, "kind": kind})
    else:
        shift_request2 = get_object_or_404(TutorShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_denied_request.html", {"shift_request": shift_request2, "kind": kind})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
# View pending requests
def view_pending_single_request(request: HttpRequest, kind: str, request_id: int) -> HttpResponse:
    if kind == "SI":
        shift_request = get_object_or_404(SIShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_pending_request.html", {"shift_request": shift_request, "kind": kind})
    else:
        shift_request2 = get_object_or_404(TutorShiftChangeRequest, id=request_id)
        return render(request, "shifts/view_pending_request.html", {"shift_request": shift_request2, "kind": kind})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def approve_pending_request(request: HttpRequest, kind: str, request_id: int) -> HttpResponse:
    request_cur = SIShiftChangeRequest.objects.get(id=request_id)
    shift = request_cur.target
    if request.method == "POST":
        form = SIApproveRequestForm(
            request.POST,
            instance=shift,
            initial={
                "associated_person": shift.associated_person,
                "start": request_cur.new_start,
                "duration": request_cur.new_duration,
            },
        )
        if form.is_valid():
            form.save()
            request_cur.request_state = "Approved"
            return HttpResponseRedirect("/scheduling/approved_shift_change_requests/SI")
    else:
        form = SIApproveRequestForm(instance=shift)

    return render(request, "scheduling/approvePendingForm.html", {"form": form, "kind": kind, "request_id": request_id})
