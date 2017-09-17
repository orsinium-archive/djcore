from django.conf import settings
from django.views import generic
from django.http import HttpResponseRedirect

from django_tables2 import RequestConfig

from .hooks4views import flat_object
from .mixins import AllMixins


class ListView(AllMixins, generic.ListView):
    context_object_name = 'objects'
    
    def get_template_names(self):
        if self.template_name is None:
            if getattr(settings, 'DJCORE_USE_BOOTSTRAP4', False):
                return 'djcore/bootstrap4/common/table.html'
            else:
                return 'djcore/bootstrap3/common/table.html'
        else:
            return [self.template_name]
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        
        table = getattr(self, 'table', None)
        if table:
            table = table(context[self.context_object_name])
            context['table'] = table
        
        return context


class InfoView(AllMixins, generic.DetailView):
    context_object_name = 'object'
    excluded_fields = ('id', 'slug', 'image', 'file')
    
    def get_template_names(self):
        if self.template_name is None:
            if getattr(settings, 'DJCORE_USE_BOOTSTRAP4', False):
                return 'djcore/bootstrap4/common/info.html'
            else:
                return 'djcore/bootstrap3/common/info.html'
        else:
            return [self.template_name]
    
    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        context['flat_object'] = flat_object(self.object, self.excluded_fields)
        return context


class DeleteView(AllMixins, generic.edit.DeleteView):
    def get_template_names(self):
        if self.template_name is None:
            if getattr(settings, 'DJCORE_USE_BOOTSTRAP4', False):
                return 'djcore/bootstrap4/common/delete.html'
            else:
                return 'djcore/bootstrap3/common/delete.html'
        else:
            return [self.template_name]
    
    def post(self, request, *args, **kwargs):
        if self.request.POST.get('confirm_delete'):
            return super(DeleteView, self).post(request, *args, **kwargs)
        elif self.request.POST.get('cancel'):
            return HttpResponseRedirect(self.success_url)
        else:
            return self.get(self, *args, **kwargs)


class AddView(AllMixins, generic.edit.CreateView):
    def get_template_names(self):
        if self.template_name is None:
            if getattr(settings, 'DJCORE_USE_BOOTSTRAP4', False):
                return 'djcore/bootstrap4/common/add.html'
            else:
                return 'djcore/bootstrap3/common/add.html'
        else:
            return [self.template_name]


class EditView(AllMixins, generic.edit.UpdateView):
    def get_template_names(self):
        if self.template_name is None:
            if getattr(settings, 'DJCORE_USE_BOOTSTRAP4', False):
                return 'djcore/bootstrap4/common/edit.html'
            else:
                return 'djcore/bootstrap3/common/edit.html'
        else:
            return [self.template_name]


class FormView(AllMixins, generic.edit.FormView):
    def get_template_names(self):
        if self.template_name is None:
            if getattr(settings, 'DJCORE_USE_BOOTSTRAP4', False):
                return 'djcore/bootstrap4/common/add.html'
            else:
                return 'djcore/bootstrap3/common/add.html'
        else:
            return [self.template_name]


class TemplateView(AllMixins, generic.base.TemplateView):
    pass


class RedirectView(AllMixins, generic.base.RedirectView):
    pass


class View(AllMixins, generic.base.View):
    pass
