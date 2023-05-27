from django.contrib import admin

from .models import Part


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('designation', 'name', 'material', 'created', 'updated')
    search_fields = ('designation', 'name')
    autocomplete_fields = ('material',)
