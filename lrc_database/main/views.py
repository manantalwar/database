import json
import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse

from .forms import EditProfileForm
from .models import Shift

User = get_user_model()
log = logging.getLogger()


def restrict_to_groups(*groups):
    def decorator(view):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.is_superuser or request.user.groups.filter(name__in=groups).exists():
                return view(request, *args, **kwargs)
            raise PermissionDenied

        return _wrapped_view

    return decorator


@login_required
def index(request):
    return render(request, "base.html")


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
    user = User.objects.get(pk=user_id)
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
def list_users(request, group):
    users = get_list_or_404(User.objects.order_by("last_name"), groups__name=group)
    return render(request, "users/list_users.html", {"users": users, "group": group})
