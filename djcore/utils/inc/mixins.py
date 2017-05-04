from functools import wraps

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

try:
	from sitetree.models import TreeItem
except (ImportError, RuntimeError):
	import warnings
	warnings.warn("Module sitetree isn't available.")
	TreeItem = False


class DecoratorsMixin:
	def dispatch(self, *args, **kwargs):
		decorators = getattr(self, 'decorators', [])
		first_base = base = super(DecoratorsMixin, self).dispatch
		
		for decorator in decorators:
			base = decorator(base)
		#base = wraps(first_base)(base)
		
		return base(*args, **kwargs)


class PermissionsMixin:
	def dispatch(self, request, *args, **kwargs):
		base = super(PermissionsMixin, self).dispatch
		
		if not TreeItem:
			return base(request, *args, **kwargs)
		
		url = current_url = request.resolver_match.view_name
		try:
			item = TreeItem.objects.get(url=url)
		except Exception as e:
			if settings.DEBUG:
				print('\x1B[32m', e, '\x1B[0m')
			return base(request, *args, **kwargs)
		
		if item.access_loggedin:
			return login_required(base)(request, *args, **kwargs)
		if getattr(item, 'access_staff', None):
			return staff_member_required(base)(request, *args, **kwargs)
		
		return base(request, *args, **kwargs)
