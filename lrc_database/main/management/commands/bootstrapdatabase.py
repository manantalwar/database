import csv
import random
from collections import defaultdict
from typing import DefaultDict

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from main.models import Course, Hardware, LRCDatabaseUser, Shift, ShiftChangeRequest

User = get_user_model()


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


def init_sis(path: str) -> None:
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        sis = list(reader)

    si_group = Group.objects.filter(name="SIs").first()

    for si in sis:
        user = User.objects.create_user(
            username=si["email"],
            email=si["email"],
            first_name=si["first_name"],
            last_name=si["last_name"],
            password=si["last_name"],
        )
        course, _ = Course.objects.update_or_create(
            department=si["course_dept"], number=int(si["course_number"]), name=si["course_name"]
        )
        """
        shift = Shift.objects.create(
            associated_person=user,
            start=timezone.datetime(2022, 11, 18, 17, 30, tzinfo=pytz.timezone("America/New_York")),
            duration=timezone.timedelta(hours=1, minutes=15),
            location="GSMN 64",
            kind="SI"
        )
        """
        user.si_course = course
        user.save()
        si_group.user_set.add(user)

    si_group.save()


def init_supervisors(path: str) -> None:
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        supervisors = list(reader)

    supervisor_group = Group.objects.filter(name="Supervisors").first()
    for supervisor in supervisors:
        user = User.objects.create_user(
            username=supervisor["email"],
            email=supervisor["email"],
            first_name=supervisor["first_name"],
            last_name=supervisor["last_name"],
            password=supervisor["last_name"],
        )
        user.save()
        supervisor_group.user_set.add(user)

    supervisor_group.save()


def init_shifts(path: str) -> None:
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        shifts = list(reader)

    for shift in shifts:
        associated_person = User.objects.filter(email=shift["email"]).first()
        start = timezone.datetime.strptime(f'{shift["date"]} {shift["start_time"]}', "%Y-%m-%d %H:%M:%S")
        start = pytz.timezone("America/New_York").localize(start)
        start_time = timezone.datetime.strptime(shift["start_time"], "%H:%M:%S")
        end_time = timezone.datetime.strptime(shift["end_time"], "%H:%M:%S")
        duration = end_time - start_time
        shift = Shift.objects.create(
            associated_person=associated_person, start=start, duration=duration, location=shift["location"], kind="SI"
        )


def init_shift_change_requests(path: str) -> None:
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        shift_change_requests = list(reader)

    for shift_change_request in shift_change_requests:
        associated_person = User.objects.filter(email=shift_change_request["email"]).first()
        start = timezone.datetime.strptime(
            f'{shift_change_request["date"]} {shift_change_request["start_time"]}', "%Y-%m-%d %H:%M:%S"
        )
        start = pytz.timezone("America/New_York").localize(start)
        start_time = timezone.datetime.strptime(shift_change_request["start_time"], "%H:%M:%S")
        end_time = timezone.datetime.strptime(shift_change_request["end_time"], "%H:%M:%S")
        duration = end_time - start_time
        ShiftChangeRequest.objects.create(
            shift_to_update=None,
            state="New",
            reason=random.choice(
                ("Final exam review", "Exam review session", "Review session", "review", "finals exam review")
            ),
            new_associated_person=associated_person,
            new_start=start,
            new_duration=duration,
            new_location=shift_change_request["location"],
            new_kind="SI",
            is_drop_request=False,
        )


def create_groups():
    print("Creating groups...")
    group_names = ("Office staff", "SIs", "Supervisors", "Tutors")
    course1, _ = Course.objects.update_or_create(
        department="TEST", number=101, name="Testing is the key I."
    )
    course2, _ = Course.objects.update_or_create(
        department="TEST", number=102, name="Testing is the key II."
    )
    for group_name in group_names:
        Group.objects.create(name=group_name)
    for user in User.objects.exclude(username="admin"):
        if user.username == "si":
            user.si_course = course1
            user.save()
            group = Group.objects.filter(name="SIs").first()
        elif user.username == "tutor":
            user.courses_tutored.add(course1)
            user.courses_tutored.add(course2)
            user.save()
            group = Group.objects.filter(name="Tutors").first()
        elif user.username == "office_staff":
            group = Group.objects.filter(name="Office staff").first()
        elif user.username == "supervisor":
            group = Group.objects.filter(name="Supervisors").first()
        else:
            continue
        group.user_set.add(user)
        group.save()


def all_of_day_in_month(year: int, month: int, weekday: int, hour: int):
    d = timezone.datetime(year, month, 1, hour, 0, 0, tzinfo=pytz.timezone("America/New_York")) + timezone.timedelta(
        days=6 - weekday
    )
    ret = []
    while d.month == month:
        ret.append(d)
        d += timezone.timedelta(days=7)
    return ret


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


"""
SELECT persons.id, persons.firstname, persons.lastname, persons.email, courses.name FROM
`persons`
LEFT JOIN `users` ON users.pid = persons.id
LEFT JOIN `role` ON role.uid = users.id
LEFT JOIN `person_course` ON person_course.pid = persons.id
LEFT JOIN `courses` ON person_course.cid = courses.id
WHERE
	persons.lastname = "THEIR LAST NAME" AND
	persons.active = 1 AND
	role.role = "si";
"""

"""
SELECT shifts.id, persons.firstname, persons.lastname, persons.email, courses.name, shifts.date, shifts.start_time, shifts.end_time, shifts.location
FROM `shifts`
    LEFT JOIN `persons` ON persons.id = shifts.pid
    LEFT JOIN `users` ON users.pid = persons.id
    LEFT JOIN `role` ON role.uid = users.id
    LEFT JOIN `person_course` ON person_course.pid = persons.id
    LEFT JOIN `courses` ON person_course.cid = courses.id
WHERE
    persons.email IN (
        "mtalwar@umass.edu", "ttpatel@umass.edu", "dsong@umass.edu", "amdawley@umass.edu", "alokhandwala@umass.edu"
    )
    AND persons.active =1
    AND role.role = "si"
    AND shifts.date >= "2022-12-01"
    AND shifts.date <= "2022-12-31"
    AND shifts.si_class =0
    AND TIMEDIFF( shifts.end_time, shifts.start_time ) <= "01:15:00"
ORDER BY persons.email, shifts.date DESC
"""


class Command(BaseCommand):
    """
    Sets up a database with some fake data.
    Example:
        manage.py bootstrapdatabase
    """

    def add_arguments(self, parser) -> None:
        parser.add_argument("--si-init-path", default="lrc_database/main/management/commands/sis.csv", type=str)
        parser.add_argument(
            "--supervisor-init-path", default="lrc_database/main/management/commands/supervisors.csv", type=str
        )
        parser.add_argument("--shift-init-path", default="lrc_database/main/management/commands/shifts.csv", type=str)
        parser.add_argument(
            "--exam-review-init-path", default="lrc_database/main/management/commands/exam_reviews.csv", type=str
        )
        parser.add_argument("--superuser-username", default="admin", type=str)
        parser.add_argument("--superuser-password", default="admin", type=str)
        parser.add_argument("--superuser-email", default="admin@umass.edu", type=str)
        parser.add_argument("--hardware-count", default=100, type=int)

    def handle(self, *args, **options):
        create_hardware(options["hardware_count"])
        create_superuser(
            options["superuser_username"],
            options["superuser_password"],
            options["superuser_email"],
        )
        create_special_users()
        create_groups()
        init_sis(options["si_init_path"])
        init_supervisors(options["supervisor_init_path"])
        init_shifts(options["shift_init_path"])
        init_shift_change_requests(options["exam_review_init_path"])
