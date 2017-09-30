# main django tools
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.core.urlresolvers import reverse, reverse_lazy

# caching
from .inc.cache import cache_page, cache_by_key

# email
from .inc.mail import Email

# views and mixins
from .inc.mixins import DecoratorsMixin, PermissionsMixin, JsonMixin
from .inc.common_views import (
    InfoView, ListView, 
    TemplateView, View, RedirectView,
    DeleteView, AddView, EditView, FormView,
    )

# some useful tools
from .inc.hooks4views import make_slug, flat_object, ChainedQueryset


# deprecated. Use PermissionsMixin.login_user and PermissionsMixin.login_staff instead
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# django sites
from django.contrib.sites.shortcuts import get_current_site

# date and time
from django.utils import timezone
import datetime

# settings
from django.conf import settings
