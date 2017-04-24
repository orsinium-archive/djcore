from sitetree.utils import item as base_item, tree

ICON_TMP = '<span class="glyphicon glyphicon-{}">{}</span>'

def item(title, url, icon=False, **kwargs):
	if icon:
		title = ICON_TMP.format(icon, title)
	return base_item(title, url, **kwargs)
