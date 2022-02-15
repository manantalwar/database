import datetime
import random
from collections import defaultdict
from typing import DefaultDict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from main.models import (
    Course,
    Hardware,
    LRCDatabaseUser,
    SISession,
    SISessionChangeRequest,
    TutoringShift,
    TutoringShiftChangeRequest,
)

User = get_user_model()
fake = Faker()

DEPARTMENTS = (
    "ACCOUNTG",
    "BIOLOGY",
    "CE-ENGIN",
    "COMPSCI",
    "FRENCHST",
    "JAPANESE",
    "MATH",
    "NUTRITN",
    "STATISTC",
)
LOCATIONS = ("ELAB", "HAS", "ILC", "LGRC", "MOR3", "TOTM")


def get_random_object(model):
    primary_keys = model.objects.values_list("pk", flat=True)
    random_pk = random.choice(primary_keys)
    random_object = model.objects.get(pk=random_pk)
    return random_object


def get_random_location() -> str:
    return f"{random.choice(LOCATIONS)} {random.randint(1, 200)}"


def create_superuser(username: str, password: str, email: str):
    User.objects.create_superuser(username=username, password=password, email=email)


def create_other_users(user_count: int):
    for _ in range(user_count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}"
        email = f"{username}@umass.edu"
        User.objects.create(
            username=username,
            password="password",
            first_name=first_name,
            last_name=last_name,
            email=email,
        )


def create_groups():
    group_names = ("Office staff", "SIs", "Supervisors", "Tutors")
    for group_name in group_names:
        Group.objects.create(name=group_name)
    for user in User.objects.exclude(username="admin"):
        random_group = get_random_object(Group)
        random_group.user_set.add(user)
        random_group.save()


def create_courses(course_count: int):
    for _ in range(course_count):
        department = random.choice(DEPARTMENTS)
        number = random.randint(100, 999)
        name = fake.text(max_nb_chars=64)
        Course.objects.create(department=department, number=number, name=name)


def create_tutoring_shifts(shift_count: int):
    for _ in range(shift_count):
        tutor = get_random_object(LRCDatabaseUser)
        location = get_random_location()
        start = timezone.now()
        duration = datetime.timedelta(hours=1)
        TutoringShift.objects.create(tutor=tutor, location=location, start=start, duration=duration)


def create_tutoring_shift_change_requests(request_count: int):
    for _ in range(request_count):
        target = get_random_object(TutoringShift)
        reason = fake.text(max_nb_chars=512)
        approved = random.random() < 0.5
        approved_by = get_random_object(LRCDatabaseUser) if approved else None
        approved_on = timezone.now() if approved else None
        new_tutor = get_random_object(LRCDatabaseUser) if random.random() < 0.25 else None
        new_start = timezone.now() if random.random() < 0.25 else None
        new_duration = datetime.timedelta(hours=2) if random.random() < 0.25 else None
        new_location = get_random_location() if random.random() < 0.25 else None
        TutoringShiftChangeRequest.objects.create(
            target=target,
            reason=reason,
            approved=approved,
            approved_by=approved_by,
            approved_on=approved_on,
            new_tutor=new_tutor,
            new_start=new_start,
            new_duration=new_duration,
            new_location=new_location,
        )


def create_si_sessions(session_count: int):
    for _ in range(session_count):
        si_leader = get_random_object(LRCDatabaseUser)
        start = timezone.now()
        duration = datetime.timedelta(hours=1)
        location = get_random_location()
        SISession.objects.create(si_leader=si_leader, start=start, duration=duration, location=location)


def create_si_session_change_requests(request_count: int):
    for _ in range(request_count):
        target = get_random_object(SISession)
        reason = fake.text(max_nb_chars=512)
        approved = random.random() < 0.5
        approved_by = get_random_object(LRCDatabaseUser) if approved else None
        approved_on = timezone.now() if approved else None
        new_si_leader = get_random_object(LRCDatabaseUser) if random.random() < 0.25 else None
        new_start = timezone.now() if random.random() < 0.25 else None
        new_duration = datetime.timedelta(hours=2) if random.random() < 0.25 else None
        new_location = get_random_location() if random.random() < 0.25 else None
        SISessionChangeRequest.objects.create(
            target=target,
            reason=reason,
            approved=approved,
            approved_by=approved_by,
            approved_on=approved_on,
            new_si_leader=new_si_leader,
            new_start=new_start,
            new_duration=new_duration,
            new_location=new_location,
        )


def create_hardware(hardware_count: int):
    HARDWARE_TYPES = ("Projector", "Calculator", "Laptop", "Power adapter")
    hardware_counts: DefaultDict[str, int] = defaultdict(int)
    for _ in range(hardware_count):
        hw_type = random.choice(HARDWARE_TYPES)
        is_available = random.random() < 0.5
        hardware_counts[hw_type] += 1
        number = hardware_counts[hw_type]
        name = f"{hw_type} #{number}"
        Hardware.objects.create(name=name, is_available=is_available)


class Command(BaseCommand):
    """
    Sets up a database with some fake data.
    Example:
        manage.py bootstrapdatabase
    """

    def add_arguments(self, parser) -> None:
        parser.add_argument("--superuser-username", default="admin")
        parser.add_argument("--superuser-password", default="admin")
        parser.add_argument("--superuser-email", default="admin@umass.edu")
        parser.add_argument("--user-count", default=100)
        parser.add_argument("--course-count", default=100)
        parser.add_argument("--tutoring-shift-count", default=100)
        parser.add_argument("--tutoring-shift-change-request-count", default=100)
        parser.add_argument("--hardware-count", default=100)
        parser.add_argument("--si-session-count", default=100)
        parser.add_argument("--si-session-change-request-count", default=100)

    def handle(self, *args, **options):
        create_hardware(options["hardware_count"])
        create_superuser(
            options["superuser_username"],
            options["superuser_password"],
            options["superuser_email"],
        )
        create_other_users(options["user_count"])
        create_groups()
        create_courses(options["course_count"])
        create_tutoring_shifts(options["tutoring_shift_count"])
        create_tutoring_shift_change_requests(options["tutoring_shift_change_request_count"])
        create_si_sessions(options["si_session_count"])
        create_si_session_change_requests(options["si_session_change_request_count"])
