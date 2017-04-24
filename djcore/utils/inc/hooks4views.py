from django.template.defaultfilters import slugify
from unidecode import unidecode

from collections import namedtuple
Field = namedtuple('Field', ['name', 'verbose_name', 'value'])

def make_slug(model, title):
	out_slug = base_slug = slugify(unidecode(title))
	counter = 2
	while model.objects.filter(slug=out_slug).exists():
		out_slug = '{}-{}'.format(base_slug, counter)
		counter += 1
	return out_slug


def flat_object(obj, excluded=''):
	rez = []
	for field in obj._meta.fields:
		if field.attname in excluded:
			continue
		value = field.value_from_object(obj)
		rez.append(Field(field.attname, field.verbose_name, value))
	return rez
