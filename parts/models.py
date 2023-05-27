from django.db import models
from materials.models import Material


class Part(models.Model):
    """Model representing a part."""

    designation = models.CharField('Designation', max_length=50, unique=True)
    name = models.CharField('Name', max_length=50)
    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name='parts',
        verbose_name='Material'
    )
    created = models.DateTimeField('Creation date', auto_now_add=True)
    updated = models.DateTimeField('Date of change', auto_now=True)

    class Meta:
        ordering = ('designation',)
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    def __str__(self):
        return f'{self.designation} - {self.name}'
