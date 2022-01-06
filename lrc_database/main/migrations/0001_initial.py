# Generated by Django 4.0 on 2022-01-06 18:32

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='LRCDatabaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(help_text='Department string, like COMPSCI or MATH.', max_length=16)),
                ('number', models.IntegerField(help_text='Course number, like the 187 in COMPSCI 187.', validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(999)])),
                ('name', models.CharField(help_text='The human-legible name of the course, like "Programming with Data Structures."', max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Hardware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('isAvailable', models.BooleanField(verbose_name=True)),
            ],
        ),
        migrations.CreateModel(
            name='TutoringShift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(help_text='The time that the session starts.')),
                ('duration', models.DurationField(help_text='How long the session will last, in HH:MM:SS format.')),
                ('location', models.CharField(help_text='The location where the session will be held, e.g. GSMN 64.', max_length=32)),
                ('tutor', models.ForeignKey(help_text='The tutor who is responsible for this session.', on_delete=django.db.models.deletion.CASCADE, to='main.lrcdatabaseuser')),
            ],
        ),
        migrations.CreateModel(
            name='TutoringShiftChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(help_text='Explanation for why this change is being requested.', max_length=512)),
                ('approved', models.BooleanField(default=False, help_text='Whether the request is approved or not.')),
                ('approved_on', models.DateTimeField(help_text='When the request was approved.')),
                ('new_start', models.DateTimeField(default=None, help_text='The new time that the session starts if this request is approved.', null=True)),
                ('new_duration', models.DurationField(default=None, help_text='How long the session will last, in HH:MM:SS format, if this request is approved.', null=True)),
                ('new_location', models.CharField(default=None, help_text='The new location where this session will be held, e.g. GSMN 64, if this request is approved.', max_length=32, null=True)),
                ('approved_by', models.ForeignKey(default=None, help_text='The user (if any) who approved the change request.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutoring_shift_change_request_approved_by', to='main.lrcdatabaseuser')),
                ('new_tutor', models.ForeignKey(default=None, help_text='The new tutor who will be responsible for the session if this request is approved.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutoring_shift_change_request_new_tutor', to='main.lrcdatabaseuser')),
                ('target', models.ForeignKey(help_text='Tutoring shift to edit.', on_delete=django.db.models.deletion.CASCADE, related_name='tutoring_shift_change_request_target', to='main.tutoringshift')),
            ],
        ),
        migrations.AddField(
            model_name='lrcdatabaseuser',
            name='courses_tutored',
            field=models.ManyToManyField(to='main.Course'),
        ),
        migrations.AddField(
            model_name='lrcdatabaseuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='lrcdatabaseuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
