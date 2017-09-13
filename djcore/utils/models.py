from django.db.models import *
from django.core.urlresolvers import reverse

from django.utils import timezone
import datetime

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from .inc.model_fields import CrossForeignKey

try:
    from ckeditor.fields import RichTextField
except (ImportError, RuntimeError):
    import warnings
    warnings.warn("Module ckeditor isn't available.")


CAN_BE_NULL = {'default': None, 'null': True, 'blank': True}


def now():
    return timezone.now()
