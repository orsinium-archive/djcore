from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy

from .inc.cache import cache_page, cache_by_key

from .inc.mail import Email
from .inc.common_views import (
    DecoratorsMixin, InfoView, ListView, TemplateView,
    DeleteView, AddView, EditView, FormView,
    )
from .inc.hooks4views import make_slug, flat_object, ChainedQueryset

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.sites.shortcuts import get_current_site

from django.utils import timezone
import datetime
