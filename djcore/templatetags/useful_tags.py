import os
import re

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

__all__ = (
	'js',
	'css',
)

register = template.Library()

def get_minified_file_path(path):
	"""
	Returns minified version file path of the given path
	if exist else return given path
	"""

	file_dir, basename = os.path.split(path)
	filename, ext = os.path.splitext(basename)

	minified_file_path = os.path.join(
		file_dir,
		"{}.min{}".format(filename, ext)
	)

	if finders.find(minified_file_path):
		return minified_file_path

	return path


def get_versioned_file_path(path):
	"""
	Versioning with query parameter prevent caching
	So versioning with mtime of file
	Serve same file with web server rewrite rule
	Example nginx rewrite rule:
	```
	location ~* \.[0-9]+\.(css|js)$ {
		rewrite (.*?)\.[0-9]+\.(css|js)$ $1.$2 last;
		access_log        off;
		expires           365d;
	}
	```
	"""
	file_path_regex = re.compile(r"^(.*)\.(.*?)$")
	mtime = int(os.path.getmtime(finders.find(path)))

	# If path: /css/main.css
	# Return same as: /css/main.1121221.css
	return file_path_regex.sub(r"\1.{}.\2".format(mtime), path)



@register.simple_tag
def js(path, **kwargs):
	"""
	A simple shortcut to render a ``script`` html tag.
	In production returns minified version of the file if exist.
	Example usage: {% js 'js/main.js' %}
	"""

	versioning = kwargs.get('versioning', True)

	if not settings.DEBUG:
		path = get_minified_file_path(path)

		if versioning:
			path = get_versioned_file_path(path)

	result = '<script type="text/javascript" src="{}"></script>'.format(
		staticfiles_storage.url(path)
	)

	return mark_safe(result)



@register.simple_tag()
def css(path, **kwargs):
	"""
	Render a ``link`` tag to a static CSS file
	In production returns minified version of the file if exist.
	Example usage: {% css 'css/style.css' %}
	"""
	versioning = kwargs.get('versioning', True)

	if not settings.DEBUG:
		path = get_minified_file_path(path)

		if versioning:
			path = get_versioned_file_path(path)
	
	result = '<link rel="stylesheet" href="{}" />'
	return mark_safe(result.format(staticfiles_storage.url(path)))
