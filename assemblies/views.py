from django.urls import reverse_lazy
from django.views import generic

from .forms import AssemblyCreateAndUpdateForm, AssemblySearchForm
from .models import Assembly


class AssemblyListView(generic.ListView):
    """Generic class-based view for a list of assemblies."""

    model = Assembly
    template_name = 'assemblies/assembly_list.html'
    context_object_name = 'assemblies'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        qs = Assembly.objects.all()
        if search_query:
            return qs.filter(designation__icontains=search_query) \
                or qs.filter(name__icontains=search_query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AssemblySearchForm(self.request.GET or None)
        return context


class AssemblyDetailView(generic.DetailView):
    """Generic class-based view for detail displaying an assembly."""

    model = Assembly
    template_name = 'assemblies/assembly_detail.html'


class AssemblyCreateView(generic.CreateView):
    """Generic class-based view for creating assembly."""

    model = Assembly
    template_name = 'assemblies/assembly_form.html'
    form_class = AssemblyCreateAndUpdateForm
    success_url = reverse_lazy('assemblies:assembly_list')
    extra_context = {
        'header': 'Assembly create',
        'title': 'Assembly create',
        'button': 'Add',
    }


class AssemblyUpdateView(generic.UpdateView):
    """Generic class-based view for updating assembly."""

    model = Assembly
    template_name = 'assemblies/assembly_form.html'
    form_class = AssemblyCreateAndUpdateForm
    success_url = reverse_lazy('assemblies:assembly_list')
    extra_context = {
        'header': 'Assembly update',
        'title': 'Assembly update',
        'button': 'Update',
    }


class AssemblyDeleteView(generic.DeleteView):
    """Generic class-based view for deleting assembly."""

    model = Assembly
    template_name = 'assemblies/assembly_delete.html'
    success_url = reverse_lazy('assemblies:assembly_list')
