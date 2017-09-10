from functools import update_wrapper

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse


try:
    from django.core.serializers import serialize
except ImportError:
    from json import dumps
    json_serialize = dumps
else:
    from functools import partial
    json_serialize = partial(serialize, 'json')


try:
    from sitetree.models import TreeItem
except (ImportError, RuntimeError):
    import warnings
    warnings.warn("Module sitetree isn't available.")
    TreeItem = False


class DecoratorsMixin(object):
    def dispatch(self, *args, **kwargs):
        decorators = getattr(self, 'decorators', [])
        first_base = base = super(DecoratorsMixin, self).dispatch
        if not decorators:
            return base(*args, **kwargs)
        
        for decorator in decorators:
            base = decorator(base)
        #take possible attributes set by decorators like csrf_exempt
        base = update_wrapper(base, first_base, assigned=())
        
        return base(*args, **kwargs)


class PermissionsMixin(object):
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


class JsonMixin(object):
    render_to_json = False
    
    def render_to_response(self, context):
        if self.render_to_json:
            data = json_serialize(context)
            return HttpResponse(data, content_type='application/json')
        else:
            super().render_to_response(context)
    
    @classmethod
    def as_json(cls):
        view = cls.as_view()
        view.render_to_json = True
        return view


class AllMixins(PermissionsMixin, DecoratorsMixin, JsonMixin):
    pass
