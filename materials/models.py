from django.db import models


class Material(models.Model):
    """Model representing a material."""

    name = models.CharField('Name', max_length=255, unique=True)
    density = models.PositiveIntegerField('Density', null=True, blank=True)
    created = models.DateTimeField('Creation date', auto_now_add=True)
    updated = models.DateTimeField('Date of change', auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'

    def __str__(self):
        return self.name
