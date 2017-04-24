from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django_tables2 import *
from urllib.parse import quote, unquote


class IntegerColumn(Column):
	def __init__(self, *args, **kwargs):
		kwargs['attrs'] = {'td': {'style': 'text-align: right;'}}
		super(IntegerColumn, self).__init__(*args, **kwargs)
	
	def render(self, value):
		return str(int(value))


class FloatColumn(IntegerColumn):
	def render(self, value):
		return '{:.2f}'.format(value)


class CountColumn(IntegerColumn):
	def render(self, value):
		value = value.filter(impact__gt=0).count()
		return super(CountColumn, self).render(value)


def make_link(url, text, blank=True):
	if blank:
		link = '<a href="{}" target="_blank">{}</a>'
	else:
		link = '<a href="{}">{}</a>'
	link = link.format(url, text)
	return mark_safe(link)
