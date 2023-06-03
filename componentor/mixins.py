from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy


class DeletionProtectionMixin:
    """Limit deletion of an object that has a reference to it."""

    success_url = reverse_lazy('home')
    success_message = 'Message about successful deletion'
    error_message = 'Deletion error message'

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(self.request, self.error_message)
            return redirect(self.success_url)
