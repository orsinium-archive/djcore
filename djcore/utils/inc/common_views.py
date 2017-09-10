from django.views import generic
from django.http import HttpResponseRedirect

from django_tables2 import RequestConfig

from .hooks4views import flat_object
from .mixins import DecoratorsMixin, PermissionsMixin


class ListView(PermissionsMixin, DecoratorsMixin, generic.ListView):
    template_name = 'djcore/common/table.html'
    context_object_name = 'objects'
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        
        table = getattr(self, 'table', None)
        if table:
            table = table(context[self.context_object_name])
            context['table'] = table
        
        return context


class InfoView(PermissionsMixin, DecoratorsMixin, generic.DetailView):
    template_name = 'djcore/common/info.html'
    context_object_name = 'object'
    excluded_fields = ('id', 'slug', 'image', 'file')
    
    def get_context_data(self, **kwargs):
        context = super(InfoView, self).get_context_data(**kwargs)
        context['flat_object'] = flat_object(self.object, self.excluded_fields)
        return context


class DeleteView(PermissionsMixin, DecoratorsMixin, generic.edit.DeleteView):
    template_name = 'djcore/common/delete.html'
    
    def post(self, request, *args, **kwargs):
        if self.request.POST.get('confirm_delete'):
            return super(DeleteView, self).post(request, *args, **kwargs)
        elif self.request.POST.get('cancel'):
            return HttpResponseRedirect(self.success_url)
        else:
            return self.get(self, *args, **kwargs)


class AddView(PermissionsMixin, DecoratorsMixin, generic.edit.CreateView):
    template_name = 'djcore/common/add.html'


class EditView(PermissionsMixin, DecoratorsMixin, generic.edit.UpdateView):
    template_name = 'djcore/common/edit.html'


class FormView(PermissionsMixin, DecoratorsMixin, generic.edit.FormView):
    template_name = 'djcore/common/add.html'


class TemplateView(PermissionsMixin, DecoratorsMixin, generic.base.TemplateView):
    pass
