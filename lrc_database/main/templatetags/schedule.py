
from django.template import Library

register = Library()

@register.filter(name='add_datetime')
def add_datetime(orignal, delta):
	return orignal + delta