import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from ..forms import CreateUserForm, CreateUsersInBulkForm, EditProfileForm
from ..models import LRCDatabaseUser, Shift
from . import restrict_to_groups, restrict_to_http_methods

User = get_user_model()


@login_required
@restrict_to_http_methods("GET")
def user_profile(request: HttpRequest, user_id: int) -> HttpResponse:
    target_user = get_object_or_404(User, id=user_id)
    target_users_shifts = json.dumps(
        list(
            map(
                lambda shift: {
                    "id": str(shift.id),
                    "start": shift.start.isoformat(),
                    "end": (shift.start + shift.duration).isoformat(),
                    "title": str(shift),
                    "allDay": False,
                    "url": reverse("view_shift", args=(shift.id,)),
                },
                Shift.objects.filter(associated_person=target_user),
            )
        )
    )

    return render(
        request,
        "users/user_profile.html",
        {"target_user": target_user, "target_users_shifts": target_users_shifts},
    )


@login_required
@restrict_to_http_methods("GET", "POST")
def edit_profile(request: HttpRequest, user_id: int) -> HttpResponse:
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
            return redirect("user_profile", user_id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("edit_profile", user_id)
    else:
        form = EditProfileForm(instance=user)
        return render(request, "users/edit_profile.html", {"user_id": user_id, "form": form})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def create_user(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = LRCDatabaseUser.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                password=form.cleaned_data["password"],
                si_course=form.cleaned_data["si_course"],
            )
            user.courses_tutored.set(form.cleaned_data["courses_tutored"])
            user.save()
            for group in form.cleaned_data["groups"]:
                group.user_set.add(user)
            return redirect("user_profile", user.id)
        else:
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("create_user")
    else:
        form = CreateUserForm()
        return render(request, "users/create_user.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET", "POST")
def create_users_in_bulk(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateUsersInBulkForm(request.POST)
        if not form.is_valid():
            messages.add_message(request, messages.ERROR, f"Form errors: {form.errors}")
            return redirect("create_users_in_bulk")
        user_data = form.cleaned_data["user_data"]
        user_data = user_data.split("\n")
        user_data = [s.strip() for s in user_data]
        user_data = [s.split(",") for s in user_data]
        for username, email, first_name, last_name, primary_group, password in user_data:
            user = LRCDatabaseUser.objects.create_user(
                username=username, email=email, first_name=first_name, last_name=last_name, password=password
            )
            groups = Group.objects.filter(name=primary_group)
            user.groups.add(*groups)
        return redirect("index")
    else:
        form = CreateUsersInBulkForm()
        return render(request, "users/create_users_in_bulk.html", {"form": form})


@restrict_to_groups("Office staff", "Supervisors")
@restrict_to_http_methods("GET")
def list_users(request: HttpRequest, group: str) -> HttpResponse:
    users = get_list_or_404(User.objects.order_by("last_name"), groups__name=group)
    return render(request, "users/list_users.html", {"users": users, "group": group})
