from django.conf.urls import url, include

PK = r'(?P<pk>\d+)'
SLUG = r'(?P<slug>[a-z0-9-]+)'

def pattern(*args):
	return r'^{}/?$'.format('/'.join(args))

def mini_url(view, *args):
	name = '_'.join([i for i in args if '?P' not in i])
	return url(pattern(*args), view.as_view(), name=name)

def list_url(view, name):
	return url(pattern(name+'s'), view.as_view(), name=name+'_list')

def info_url(view, name, pk=PK):
	return url(pattern(name, pk), view.as_view(), name=name+'_info')
