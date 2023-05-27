from django.contrib import admin
from materials import models


@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')
    search_fields = ('name', 'created')
