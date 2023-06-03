import componentor.mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from materials.forms import MaterialCreateAndUpdateForm, MaterialSearchForm
from materials.models import Material


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


class MaterialCreateView(SuccessMessageMixin, generic.CreateView):
    """Generic class-based view for creating material."""

    model = Material
    template_name = 'materials/material_form.html'
    form_class = MaterialCreateAndUpdateForm
    success_url = reverse_lazy('materials:material_list')
    success_message = 'The material successfully created'
    extra_context = {
        'header': 'Material create',
        'title': 'Material create',
        'button': 'Add',
    }


class MaterialUpdateView(SuccessMessageMixin, generic.UpdateView):
    """Generic class-based view for updating material."""

    model = Material
    template_name = 'materials/material_form.html'
    form_class = MaterialCreateAndUpdateForm
    success_message = 'The material successfully updated'
    extra_context = {
        'header': 'Material update',
        'title': 'Material update',
        'button': 'Update',
    }

    def get_success_url(self):
        material_id = self.object.pk
        return reverse_lazy(
            'materials:material_detail', kwargs={'pk': material_id}
        )


class MaterialDeleteView(componentor.mixins.DeletionProtectionMixin,
                         generic.DeleteView):
    """Generic class-based view for deleting material."""

    model = Material
    template_name = 'materials/material_delete.html'
    success_url = reverse_lazy('materials:material_list')
    success_message = 'The material successfully deleted'
    error_message = "Can't delete material because it's in use"
