from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from sitetree.models import TreeItem
from django.conf.settings import DEBUG


class DecoratorsMixin:
	def dispatch(self, *args, **kwargs):
		decorators = getattr(self, 'decorators', [])
		base = super(DecoratorsMixin, self).dispatch
		
		for decorator in decorators:
			base = decorator(base)
		return base(*args, **kwargs)


class PermissionsMixin:
	def dispatch(self, request, *args, **kwargs):
		decorators = getattr(self, 'decorators', [])
		base = super(PermissionsMixin, self).dispatch
		
		url = current_url = request.resolver_match.view_name
		try:
			item = TreeItem.objects.get(url=url)
		except Exception as e:
			if DEBUG:
				print('\x1B[32m', e, '\x1B[0m')
			return base(request, *args, **kwargs)
		
		if item.access_loggedin:
			return login_required(base)(request, *args, **kwargs)
		if getattr(item, 'access_staff', None):
			return staff_member_required(base)(request, *args, **kwargs)
		
		return base(request, *args, **kwargs)
