import materials.models
from assemblies import forms
from assemblies.models import Assembly
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic


class AssemblyInline:
    form_class = forms.AssemblyCreateAndUpdateForm
    model = Assembly
    template_name = 'assemblies/assembly_form.html'

    def get_success_url(self):
        return reverse_lazy('assemblies:assembly_list')

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, f'formset_{name}_valid', None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect(self.get_success_url())

    def formset_parts_valid(self, formset):
        parts = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()
        for part in parts:
            part.assembly = self.object
            part.save()


class AssemblyCreateView(SuccessMessageMixin,
                         AssemblyInline,
                         generic.CreateView):
    """Generic class-based view for creating assembly."""

    success_message = 'The assembly successfully created'

    def get_context_data(self, **kwargs):
        context = super(AssemblyCreateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context.update(
            {
                'header': 'Assembly create',
                'title': 'Assembly create',
                'button': 'Add',
            }
        )
        return context

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {'parts': forms.PartFormset(prefix='parts')}
        else:
            return {
                'parts': forms.PartFormset(
                    self.request.POST or None,
                    prefix='parts',
                )
            }


class AssemblyUpdateView(SuccessMessageMixin,
                         AssemblyInline,
                         generic.UpdateView):
    """Generic class-based view for updating assembly."""

    success_message = 'The assembly successfully updated'

    def get_success_url(self):
        assembly_id = self.object.pk
        return reverse_lazy(
            'assemblies:assembly_detail', kwargs={'pk': assembly_id}
        )

    def get_context_data(self, **kwargs):
        context = super(AssemblyUpdateView, self).get_context_data(**kwargs)
        context['named_formsets'] = self.get_named_formsets()
        context.update(
            {
                'header': 'Assembly update',
                'title': 'Assembly update',
                'button': 'Update',
            }
        )
        return context

    def get_named_formsets(self):
        return {
            'parts': forms.PartFormset(
                self.request.POST or None,
                instance=self.object,
                prefix='parts',
            )
        }


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
        context['form'] = forms.AssemblySearchForm(self.request.GET or None)
        return context


class AssemblyDetailView(generic.DetailView):
    """Generic class-based view for detail displaying an assembly."""

    model = Assembly
    template_name = 'assemblies/assembly_detail.html'

    def get_parts_in_assembly(self):
        search_query = self.request.GET.get('search_query', '')
        all_material_parts = materials.models.Material.objects\
            .filter(name__icontains=search_query)\
            .values_list('parts', flat=True)
        material_parts_id_in_assembly = self.object.assemblypart_set\
            .values_list('part', flat=True)\
            .filter(part__in=all_material_parts)
        parts_in_assembly = self.object.assemblypart_set\
            .filter(part__in=material_parts_id_in_assembly)
        return parts_in_assembly

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.AssemblyPartSearchForm(self.request.GET or None)
        context['parts'] = self.get_parts_in_assembly()
        return context


class AssemblyDeleteView(SuccessMessageMixin, generic.DeleteView):
    """Generic class-based view for deleting assembly."""

    model = Assembly
    template_name = 'assemblies/assembly_delete.html'
    success_url = reverse_lazy('assemblies:assembly_list')
    success_message = 'The assembly successfully deleted'
