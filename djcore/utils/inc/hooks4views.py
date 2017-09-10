from django.template.defaultfilters import slugify
try:
    from unidecode import unidecode
except ImportError:
    import warnings
    unidecode = False
    warnings.warn("Module unidecode isn't available.")


from collections import namedtuple
Field = namedtuple('Field', ['name', 'verbose_name', 'value'])


def make_slug(title, model=False):
    if unidecode:
        title = unidecode(title)
    out_slug = base_slug = slugify(title)
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


class ChainedQueryset:
    
    def __init__(self, *querysets):
        self.querysets = querysets
        self._count = sum([q.count() for q in querysets])
    
    def count(self):
        return self._count
    
    def __len__(self):
        return self._count
    
    def __list__(self):
        return sum(map(list, self.querysets), [])
    
    def iterator(self):
        for  queryset in self.querysets:
            yield from queryset.iterator()
    
    def __getitem__(self, index):
        return self.__list__()[index]
