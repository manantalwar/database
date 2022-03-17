from django import template

register = template.Library()


def is_in_groups(user, *groups):
    return user.is_authenticated and user.groups.filter(name__in=groups).exists()


@register.filter
def is_si(user):
    return is_in_groups(user, "SIs")


@register.filter
def is_tutor(user):
    return is_in_groups(user, "Tutors")


@register.filter
def is_office_staff(user):
    return is_in_groups(user, "Office staff")


@register.filter
def is_supervisor(user):
    return is_in_groups(user, "Supervisors")


@register.filter
def is_privileged(user):
    """
    Is the user someone who should have privileges to, say, view all users or
    add shifts to someone else? Currently, this just asks whether the user is
    office staff or a supervisor.

    This should probably be renamed at some point.
    """
    return is_in_groups(user, "Office staff", "Supervisors")
