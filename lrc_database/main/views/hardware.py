from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from ..forms import AddHardwareForm, NewLoanForm
from ..models import Hardware, Loan
from . import restrict_to_groups, restrict_to_http_methods


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def show_hardware(request: HttpRequest) -> HttpResponse:
    hardware = Hardware.objects.order_by("name")
    curLoans = Loan.objects.all()
    return render(
        request,
        "hardware/hardware_table.html",
        {"hardware": hardware, "curLoans": curLoans},
    )


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def show_loans(request: HttpRequest) -> HttpResponse:
    loanInfo = Loan.objects.order_by("return_time")
    return render(request, "loans/show_loans.html", {"loanInfo": loanInfo})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def add_hardware(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AddHardwareForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        return redirect("show_hardware")
    else:
        form = AddHardwareForm()
        context = {"form": form}
    return render(request, "hardware/add_hardware.html", context)


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def add_loans(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = NewLoanForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("show_loans")
    else:
        form = NewLoanForm()
    context = {"form": form}
    return render(request, "loans/add_loans.html", context)


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def edit_loans(request: HttpRequest, loan_id: int) -> HttpResponse:
    loan1 = Loan.objects.get(id=loan_id)
    if request.method == "POST":
        form = NewLoanForm(request.POST, instance=loan1)
        if form.is_valid():
            form.save()
            return redirect("show_loans")
    else:
        form = NewLoanForm(instance=loan1)

    return render(request, "loans/edit_loans.html", {"form": form, "loan_id": loan_id})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def edit_hardware(request: HttpRequest, hardware_id: int) -> HttpResponse:
    hardware1 = Hardware.objects.get(id=hardware_id)
    if request.method == "POST":
        form = AddHardwareForm(request.POST, instance=hardware1)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("show_hardware")
    else:
        form = AddHardwareForm(instance=hardware1)
    context = {"form": form, "hardware_id": hardware_id}
    return render(request, "hardware/edit_hardware.html", context)
