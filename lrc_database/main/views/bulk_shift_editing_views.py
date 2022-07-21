from django import forms
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..models import Shift
from . import restrict_to_groups, restrict_to_http_methods


class DropShiftsOnDateForm(forms.Form):
    date = forms.DateField()


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def drop_shifts_on_date(request: HttpRequest) -> HttpResponse:
    form = DropShiftsOnDateForm()
    return render(request, "shifts/drop_shifts_on_date.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def drop_shifts_on_date_confirmation(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = DropShiftsOnDateForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, f"Form has errors: {form.errors}")
            return redirect("drop_shifts_on_date")
        date = form.cleaned_data["date"]
        shifts = Shift.objects.filter(start__year=date.year, start__month=date.month, start__day=date.day)
        request.session["shift_keys"] = list(shifts.values_list("id", flat=True))
        return render(request, "shifts/drop_shifts_on_date_confirmation.html", {"affected_shifts": shifts})
    else:
        shift_keys = request.session.get("shift_keys", [])
        shifts = Shift.objects.filter(id__in=shift_keys)
        deleted_count, _ = shifts.delete()
        messages.add_message(request, messages.INFO, f"Deleted {deleted_count} shifts.")
        return redirect("drop_shifts_on_date")
