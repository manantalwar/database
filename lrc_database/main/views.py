from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_list_or_404, get_object_or_404, render

from .models import Shift

User = get_user_model()


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
    return render(
        request, "user_profile.html", {"target_user": target_user, "target_users_shifts": target_users_shifts}
    )


@restrict_to_groups("Office staff", "Supervisors")
def list_users(request, group):
    users = get_list_or_404(User.objects.order_by("last_name"), groups__name=group)
    return render(request, "list_users.html", {"users": users, "group": group})
