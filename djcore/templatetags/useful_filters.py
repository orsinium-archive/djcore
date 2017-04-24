# coding: utf-8
import json

from django import template
from django.utils.dateparse import parse_datetime
from django.utils.html import mark_safe


register = template.Library()


@register.filter
def get_range(value, start_from=0):
	"""
	Filter - returns a list containing range made from given value
	Usage (in template):
	<ul>{% for i in 3|get_range %}
		<li>{{ i }}. Do something</li>
	{% endfor %}</ul>
	Results with the HTML:
	<ul>
		<li>0. Do something</li>
		<li>1. Do something</li>
		<li>2. Do something</li>
	</ul>
	Instead of 3 one may use the variable set in the views
	"""

	return range(start_from, value)


@register.filter('parse_datetime')
def parse_datetime_filter(date_string):
	"""
	Return a datetime corresponding to date_string, parsed according to DATETIME_INPUT_FORMATS
	For example, to re-display a date string in another format::
	{{ "01/01/1970"|parse_datetime|date:"F jS, Y" }}
	"""

	try:
		return parse_datetime(date_string)
	except Exception:
		return date_string


@register.filter
def toJSON(value):
	return mark_safe(json.dumps(value))


@register.filter
def addcss(field, arg):
	"""
		Add class to field in templates
		{{ field|addcss:'my-class' }}
	"""
	return field.as_widget(attrs={'class': arg})
