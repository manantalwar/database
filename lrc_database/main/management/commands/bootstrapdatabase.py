import random
from collections import defaultdict
from typing import DefaultDict

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from main.models import Course, Hardware, LRCDatabaseUser, Shift, SIShiftChangeRequest, TutorShiftChangeRequest

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
    print("Creating superuser...")
    User.objects.create_superuser(username=username, password=password, email=email)


def create_special_users():
    print("Creating special users...")
    User.objects.create_user(
        username="si",
        password="password",
        first_name="Test SI",
        last_name="user",
    )
    User.objects.create_user(
        username="tutor",
        password="password",
        first_name="Test Tutor",
        last_name="user",
    )
    User.objects.create_user(
        username="office_staff",
        password="password",
        first_name="Test Office Staff",
        last_name="user",
    )
    User.objects.create_user(
        username="supervisor",
        password="password",
        first_name="Test Supervisor",
        last_name="user",
    )


def create_other_users(user_count: int):
    print("Creating other users...")
    for _ in range(user_count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}"
        email = f"{username}@umass.edu"
        User.objects.create_user(
            username=username,
            password="password",
            first_name=first_name,
            last_name=last_name,
            email=email,
        )


def create_groups():
    print("Creating groups...")
    group_names = ("Office staff", "SIs", "Supervisors", "Tutors")
    for group_name in group_names:
        Group.objects.create(name=group_name)
    for user in User.objects.exclude(username="admin"):
        if user.username == "si":
            group = Group.objects.filter(name="SIs").first()
        elif user.username == "tutor":
            group = Group.objects.filter(name="Tutors").first()
        elif user.username == "office_staff":
            group = Group.objects.filter(name="Office staff").first()
        elif user.username == "supervisor":
            group = Group.objects.filter(name="Supervisors").first()
        else:
            group = get_random_object(Group)
        group.user_set.add(user)
        group.save()


def create_courses(course_count: int):
    print("Creating courses...")
    for _ in range(course_count):
        department = random.choice(DEPARTMENTS)
        number = random.randint(100, 999)
        name = fake.text(max_nb_chars=64)
        Course.objects.create(department=department, number=number, name=name)


def create_tutor_course_associations(courses_per_tutor: int):
    print("Creating tutor/course associations...")
    for tutor in LRCDatabaseUser.objects.filter(groups__name="Tutors"):
        for _ in range(courses_per_tutor):
            tutor.courses_tutored.add(get_random_object(Course))


def create_si_course_associations():
    print("Creating SI/course associations...")
    for si in LRCDatabaseUser.objects.filter(groups__name="SIs"):
        si.si_course = get_random_object(Course)
        si.save()


def all_of_day_in_month(year: int, month: int, weekday: int, hour: int):
    d = timezone.datetime(year, month, 1, hour, 0, 0, tzinfo=pytz.UTC) + timezone.timedelta(days=6 - weekday)
    ret = []
    while d.month == month:
        ret.append(d)
        d += timezone.timedelta(days=7)
    return ret


def create_shifts():
    print("Creating shifts...")
    users = LRCDatabaseUser.objects.all()
    current_year = timezone.now().year
    current_month = timezone.now().month
    for user in users:
        group = user.groups.first()
        if not group or group.name not in ("SIs", "Tutors"):
            continue
        group = group.name
        location = get_random_location()
        weekday_1 = random.randint(0, 6)
        weekday_2 = random.randint(0, 6)
        hour_1 = random.randint(0, 23)
        hour_2 = random.randint(0, 23)
        shift_times = all_of_day_in_month(current_year, current_month, weekday_1, hour_1) + all_of_day_in_month(
            current_year, current_month, weekday_2, hour_2
        )
        print(group)
        kind = "SI" if group == "SIs" else "Tutoring"
        for shift_time in shift_times:
            Shift.objects.create(
                associated_person=user,
                location=location,
                start=shift_time,
                duration=timezone.timedelta(hours=1),
                kind=kind,
            )


def create_si_shift_change_requests(request_count: int):
    print("Creating shift change requests...")
    for _ in range(request_count):
        target = get_random_object(Shift)
        reason = fake.text(max_nb_chars=512)
        type = ("Approved", "Not Approved", "Pending", "New")
        request_state = random.choice(type)
        approved_by = get_random_object(LRCDatabaseUser) if type == "Approved" else None
        approved_on = timezone.now() if type == "Approved" else None
        new_start = timezone.now() if random.random() < 0.25 else None
        new_duration = timezone.timedelta(hours=2) if random.random() < 0.25 else None
        new_location = get_random_location() if random.random() < 0.25 else None
        SIShiftChangeRequest.objects.create(
            target=target,
            reason=reason,
            request_state=request_state,
            approved_by=approved_by,
            approved_on=approved_on,
            new_start=new_start,
            new_duration=new_duration,
            new_location=new_location,
        )


def create_tutor_shift_change_requests(request_count: int):
    print("Creating shift change requests...")
    for _ in range(request_count):
        target = get_random_object(Shift)
        reason = fake.text(max_nb_chars=512)
        type = ("Approved", "Not Approved", "New")
        request_state = random.choice(type)
        approved_by = get_random_object(LRCDatabaseUser) if type == "Approved" else None
        approved_on = timezone.now() if type == "Approved" else None
        new_associated_person = get_random_object(LRCDatabaseUser) if random.random() < 0.25 else None
        new_start = timezone.now() if random.random() < 0.25 else None
        new_duration = timezone.timedelta(hours=2) if random.random() < 0.25 else None
        new_location = get_random_location() if random.random() < 0.25 else None
        TutorShiftChangeRequest.objects.create(
            target=target,
            reason=reason,
            request_state=request_state,
            approved_by=approved_by,
            approved_on=approved_on,
            new_associated_person=new_associated_person,
            new_start=new_start,
            new_duration=new_duration,
            new_location=new_location,
        )


def create_hardware(hardware_count: int):
    print("Creating hardware...")
    HARDWARE_TYPES = (
        "Projector",
        "Calculator",
        "Laptop",
        "Power adapter",
    )
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
        parser.add_argument("--superuser-username", default="admin", type=str)
        parser.add_argument("--superuser-password", default="admin", type=str)
        parser.add_argument("--superuser-email", default="admin@umass.edu", type=str)
        parser.add_argument("--user-count", default=10, type=int)
        parser.add_argument("--course-count", default=25, type=int)
        parser.add_argument("--courses-per-tutor", default=3, type=int)
        parser.add_argument("--shift-change-request-count", default=100, type=int)
        parser.add_argument("--hardware-count", default=100, type=int)

    def handle(self, *args, **options):
        create_hardware(options["hardware_count"])
        create_superuser(
            options["superuser_username"],
            options["superuser_password"],
            options["superuser_email"],
        )
        create_special_users()
        create_other_users(options["user_count"])
        create_groups()
        create_courses(options["course_count"])
        create_tutor_course_associations(options["courses_per_tutor"])
        create_si_course_associations()
        create_shifts()
        create_si_shift_change_requests(options["shift_change_request_count"])
        create_tutor_shift_change_requests(options["shift_change_request_count"])
