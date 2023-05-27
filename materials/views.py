from django.urls import reverse_lazy
from django.views import generic

from .forms import MaterialCreateAndUpdateForm, MaterialSearchForm
from .models import Material


class MaterialListView(generic.ListView):
    """Generic class-based view for a list of materials."""

    model = Material
    template_name = 'materials/material_list.html'
    context_object_name = 'materials'

    def get_queryset(self):
        name = self.request.GET.get('name')
        qs = Material.objects.all()
        if name:
            return qs.filter(name__icontains=name)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MaterialSearchForm(self.request.GET or None)
        return context


class MaterialDetailView(generic.DetailView):
    """Generic class-based view for detail displaying a material."""

    model = Material
    template_name = 'materials/material_detail.html'


class MaterialCreateView(generic.CreateView):
    """Generic class-based view for creating material."""

    model = Material
    template_name = 'materials/material_form.html'
    form_class = MaterialCreateAndUpdateForm
    success_url = reverse_lazy('materials:material_list')
    extra_context = {
        'header': 'Material create',
        'title': 'Material create',
        'button': 'Add',
    }


class MaterialUpdateView(generic.UpdateView):
    """Generic class-based view for updating material."""

    model = Material
    template_name = 'materials/material_form.html'
    form_class = MaterialCreateAndUpdateForm
    success_url = reverse_lazy('materials:material_list')
    extra_context = {
        'header': 'Material update',
        'title': 'Material update',
        'button': 'Update',
    }


class MaterialDeleteView(generic.DeleteView):
    """Generic class-based view for deleting material."""

    model = Material
    template_name = 'materials/material_delete.html'
    success_url = reverse_lazy('materials:material_list')
