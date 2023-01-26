from datetime import datetime, timedelta
from urllib import request
import pytz

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..models import Shift, Course
from . import restrict_to_groups, restrict_to_http_methods

timezone = pytz.timezone("America/New_York")

@login_required
@restrict_to_http_methods("GET")
@restrict_to_groups("Office staff", "Supervisors")
def view_schedule(request: HttpRequest, kind: str, offset: str) -> HttpResponse:
	offset = int(offset)

	today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone)
	start = today + timedelta(days=offset)
	end = start + timedelta(days=7)

	shifts = Shift.objects.filter(start__gte=start.isoformat(), start__lte=end)

	weekdays = [start + i*timedelta(days=1) for i in range(7)]

	info = {}

	courses = Course.objects.all()

	for course in courses:
		info[course.short_name()] = [course.id,[[],[],[],[],[],[],[]]]

	start_day = start.weekday()

	for shift in shifts:
		s_kind = shift.kind
		s_person = shift.associated_person
		if s_kind == "SI" and (kind == "SI" or kind == "All"):
			s_course = s_person.si_course.short_name()
			info[s_course][1][(shift.start.weekday()-start_day)%7].append(shift)
		elif kind == "Tutoring" or kind == "All":
			for course in s_person.courses_tutored.all():
				info[course.short_name()][1][(shift.start.weekday()-start_day)%7].append(shift)

	return render(request, "schedule/schedule_view.html", {"kind": kind, "offset": offset, "weekdays": weekdays, "info": info})