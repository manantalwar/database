# Generated by Django 4.1.3 on 2022-12-13 13:52

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="LRCDatabaseUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={"unique": "A user with that username already exists."},
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                        verbose_name="username",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("department", models.CharField(help_text="Department string, like COMPSCI or MATH.", max_length=16)),
                (
                    "number",
                    models.IntegerField(
                        help_text="Course number, like the 187 in COMPSCI 187.",
                        validators=[
                            django.core.validators.MinValueValidator(100),
                            django.core.validators.MaxValueValidator(999),
                        ],
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text='The human-legible name of the course, like "Programming with Data Structures."',
                        max_length=64,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Hardware",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("is_available", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name_plural": "hardware",
            },
        ),
        migrations.CreateModel(
            name="Shift",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start", models.DateTimeField(help_text="The time that the shift starts.")),
                ("duration", models.DurationField(help_text="How long the shift will last, in HH:MM:SS format.")),
                (
                    "location",
                    models.CharField(
                        help_text="The location where the shift will be occur, e.g. GSMN 64.", max_length=32
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[("SI", "SI"), ("Tutoring", "Tutoring")],
                        help_text="The kind of shift this is: tutoring or SI.",
                        max_length=8,
                    ),
                ),
                (
                    "associated_person",
                    models.ForeignKey(
                        help_text="The person who is associated with this work shift.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ShiftChangeRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "reason",
                    models.CharField(
                        help_text="Explanation for why this new shift or shift change is being requested.",
                        max_length=512,
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("Approved", "Approved"),
                            ("Pending", "Pending"),
                            ("Not Approved", "Not Approved"),
                            ("New", "New"),
                        ],
                        help_text="The kind of shift this is.",
                        max_length=40,
                    ),
                ),
                ("is_drop_request", models.BooleanField(default=False)),
                (
                    "new_start",
                    models.DateTimeField(
                        blank=True,
                        default=None,
                        help_text="The date time that the shift starts if this request is approved, in 24-hour YYYY-MM-DD HH:MM:SS format.",
                        null=True,
                    ),
                ),
                (
                    "new_duration",
                    models.DurationField(
                        blank=True,
                        default=None,
                        help_text="How long the shift will last, in HH:MM:SS format, if this request is approved.",
                        null=True,
                    ),
                ),
                (
                    "new_location",
                    models.CharField(
                        blank=True,
                        default=None,
                        help_text="The location where this shift will occur, e.g. GSMN 64, if this request is approved.",
                        max_length=32,
                        null=True,
                    ),
                ),
                (
                    "new_kind",
                    models.CharField(
                        blank=True,
                        choices=[("SI", "SI"), ("Tutoring", "Tutoring")],
                        default=None,
                        help_text="The kind of shift this is: tutoring or SI.",
                        max_length=8,
                        null=True,
                    ),
                ),
                (
                    "new_associated_person",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="The person who is associated with this work shift.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "shift_to_update",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="Shift to edit. If none, this change request will create a new shift when approved.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shift_change_request_target",
                        to="main.shift",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Loan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_time", models.DateTimeField(help_text="DD/MM/YYYY HH:MM")),
                (
                    "return_time",
                    models.DateTimeField(blank=True, default=None, help_text="DD/MM/YYYY HH:MM", null=True),
                ),
                (
                    "hardware_user",
                    models.ForeignKey(
                        help_text="LRC USER", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "target",
                    models.ForeignKey(
                        help_text="REQUESTED HARDWARE",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="intended_hardware_to_borrow",
                        to="main.hardware",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="lrcdatabaseuser",
            name="courses_tutored",
            field=models.ManyToManyField(blank=True, default=None, to="main.course"),
        ),
        migrations.AddField(
            model_name="lrcdatabaseuser",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="lrcdatabaseuser",
            name="si_course",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="lrc_database_user_si_course",
                to="main.course",
                verbose_name="SI course",
            ),
        ),
        migrations.AddField(
            model_name="lrcdatabaseuser",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
