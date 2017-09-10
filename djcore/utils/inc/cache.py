from django.views.decorators.cache import cache_page

def default_key(request):
    is_staff = int(request.user.is_staff)
    is_auth = int(request.user.is_authenticated())
    return '_auth_{}{}_'.format(is_staff, is_auth)

class cache_by_key:
    
    #создаем декоратор
    def __init__(self, *args, key=None, **kwargs):
        self.dec_args = args
        self.dec_kwargs = kwargs
        if key:
            self.key = key
        else:
            self.key = default_key
    
    #декорируем view
    def __call__(self, view_func):
        def _wrapped_view(request, *args, **kwargs):
            new_dec = cache_page(*self.dec_args,
                key_prefix=self.key(request), **self.dec_kwargs)
            return new_dec(view_func)(request, *args, **kwargs)
        return _wrapped_view
