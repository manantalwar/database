from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_course_number(value):
	class_number = None
	try:
		class_number = "0"
		for c in value.split():
			if c.isdigit():
				class_number += c
			else:
				break
		class_number = int(class_number)
	except:
		raise ValidationError(_('First 3 characters of course number should be a number'))

	if class_number < 100 or class_number > 999:
		raise ValidationError(_('Course number should be between 100 and 999'))