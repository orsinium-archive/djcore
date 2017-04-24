from django.template.defaultfilters import slugify
from unidecode import unidecode

from collections import namedtuple
Field = namedtuple('Field', ['name', 'verbose_name', 'value'])

def make_slug(title, model=False):
	out_slug = base_slug = slugify(unidecode(title))
	counter = 2
	
	if not model:
		return out_slug
	
	while model.objects.filter(slug=out_slug).exists():
		out_slug = '{}-{}'.format(base_slug, counter)
		counter += 1
	
	return out_slug


def flat_object(obj, excluded=''):
	result = []
	for field in obj._meta.fields:
		if field.attname in excluded:
			continue
		value = field.value_from_object(obj)
		result.append(Field(field.attname, field.verbose_name, value))
	return result
