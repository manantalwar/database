from typing import DefaultDict
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from collections import defaultdict
import datetime
import random

from main.models import Course, Hardware, LRCDatabaseUser, TutoringShift


User = get_user_model()
fake = Faker()


def get_random_object(model):
    primary_keys = model.objects.values_list('pk', flat=True)
    random_pk = random.choice(primary_keys)
    random_object = model.objects.get(pk=random_pk)
    return random_object


def create_superuser(username: str, password: str):
    User.objects.create_superuser(username=username, password=password)


def create_other_users(user_count: int):
    for _ in range(user_count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name.lower()}{last_name.lower()}'
        email = f'{username}@umass.edu'
        User.objects.create(username=username, password='password', first_name=first_name, last_name=last_name, email=email)


def create_courses(course_count: int):
    DEPARTMENTS = ('ACCOUNTG', 'BIOLOGY', 'CE-ENGIN', 'COMPSCI', 'FRENCHST', 'JAPANESE', 'MATH', 'NUTRITN', 'STATISTC')
    for _ in range(course_count):
        department = random.choice(DEPARTMENTS)
        number = random.randint(100, 999)
        name = fake.text(max_nb_chars=64)
        Course.objects.create(department=department, number=number, name=name)


def create_tutoring_shifts(shift_count: int):
    LOCATIONS = ('ELAB', 'HAS', 'ILC', 'LGRC', 'MOR3', 'TOTM')
    for _ in range(shift_count):
        tutor = get_random_object(LRCDatabaseUser)
        location = f'{random.choice(LOCATIONS)} {random.randint(1, 200)}'
        start = timezone.now()
        duration = datetime.timedelta(hours=1)
        TutoringShift.objects.create(tutor=tutor, location=location, start=start, duration=duration)


def create_hardware(hardware_count: int):
    HARDWARE_TYPES = ('Projector', 'Calculator', 'Laptop', 'Power adapter')
    hardware_counts: DefaultDict[str, int] = defaultdict(int)
    for _ in range(hardware_count):
        hw_type = random.choice(HARDWARE_TYPES)
        is_available = random.random() < 0.5
        hardware_counts[hw_type] += 1
        number = hardware_counts[hw_type]
        name = f'{hw_type} #{number}'
        Hardware.objects.create(name=name, is_available=is_available)


class Command(BaseCommand):
    """
    Sets up a database with some fake data.
    Example:
        manage.py bootstrapdatabase
    """

    def add_arguments(self, parser) -> None:
        parser.add_argument('--superuser-username', default='admin')
        parser.add_argument('--superuser-password', default='admin')
        parser.add_argument('--user-count', default=100)
        parser.add_argument('--course-count', default=100)
        parser.add_argument('--tutoring-shift-count', default=100)
        parser.add_argument('--hardware-count', default=100)

    def handle(self, *args, **options):
        create_hardware(options['hardware_count'])
        create_superuser(options['superuser_username'], options['superuser_password'])
        create_other_users(options['user_count'])
        create_courses(options['course_count'])
        create_tutoring_shifts(options['tutoring_shift_count'])
