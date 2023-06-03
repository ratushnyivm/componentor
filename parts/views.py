import componentor.mixins
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from parts.forms import PartCreateAndUpdateForm, PartSearchForm
from parts.models import Part


class PartListView(generic.ListView):
    """Generic class-based view for a list of parts."""

    model = Part
    template_name = 'parts/part_list.html'
    context_object_name = 'parts'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        qs = Part.objects.all()
        if search_query:
            return qs.filter(designation__icontains=search_query) \
                or qs.filter(name__icontains=search_query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PartSearchForm(self.request.GET or None)
        return context


class PartDetailView(generic.DetailView):
    """Generic class-based view for detail displaying a part."""

    model = Part
    template_name = 'parts/part_detail.html'


class PartCreateView(SuccessMessageMixin, generic.CreateView):
    """Generic class-based view for creating part."""

    model = Part
    template_name = 'parts/part_form.html'
    form_class = PartCreateAndUpdateForm
    success_url = reverse_lazy('parts:part_list')
    success_message = 'The part successfully created'
    extra_context = {
        'header': 'Part create',
        'title': 'Part create',
        'button': 'Add',
    }


class PartUpdateView(SuccessMessageMixin, generic.UpdateView):
    """Generic class-based view for updating part."""

    model = Part
    template_name = 'parts/part_form.html'
    form_class = PartCreateAndUpdateForm
    success_message = 'The part successfully updated'
    extra_context = {
        'header': 'Part update',
        'title': 'Part update',
        'button': 'Update',
    }

    def get_success_url(self):
        part_id = self.object.pk
        return reverse_lazy(
            'parts:part_detail', kwargs={'pk': part_id}
        )


class PartDeleteView(componentor.mixins.DeletionProtectionMixin,
                     generic.DeleteView):
    """Generic class-based view for deleting part."""

    model = Part
    template_name = 'parts/part_delete.html'
    success_url = reverse_lazy('parts:part_list')
    success_message = 'The part successfully deleted'
    error_message = "Can't delete part because it's in use"
