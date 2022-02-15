from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_list_or_404, render

User = get_user_model()


def restrict_to_groups(groups):
    def decorator(view):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if type(groups) is str:
                match = request.user.groups.filter(name=groups).exists()
            else:
                match = request.user.groups.filter(name__in=groups).exists()
            if match:
                return view(request, *args, **kwargs)
            raise PermissionDenied

        return _wrapped_view

    return decorator


@login_required
def index(request):
    return render(request, "base.html")


@restrict_to_groups(["Office staff", "Supervisors"])
def list_users(request, group):
    users = get_list_or_404(User, groups__name=group)
    return render(request, "list_users.html", {"users": users, "group": group})
