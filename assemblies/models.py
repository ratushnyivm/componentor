from django.core.validators import MinValueValidator
from django.db import models
from parts.models import Part


class Assembly(models.Model):
    """Model representing an assembly."""

    designation = models.CharField('Designation', max_length=50, unique=True)
    name = models.CharField('Name', max_length=50)
    parts = models.ManyToManyField(
        Part,
        blank=True,
        verbose_name='Parts',
        through="AssemblyPart",
    )
    created = models.DateTimeField('Creation date', auto_now_add=True)
    updated = models.DateTimeField('Date of change', auto_now=True)

    class Meta:
        ordering = ('designation',)
        verbose_name = 'Assembly'
        verbose_name_plural = 'Assemblies'

    def __str__(self):
        return f'{self.designation} - {self.name}'


class AssemblyPart(models.Model):
    """Model representing intermediary table linking parts to assemblies."""

    assembly = models.ForeignKey(
        Assembly,
        on_delete=models.CASCADE,
        verbose_name='Assembly',
    )
    part = models.ForeignKey(
        Part,
        on_delete=models.PROTECT,
        verbose_name='Part',
    )
    part_count = models.IntegerField(
        'Quantity',
        default=1,
        validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = 'Part in assembly'
        verbose_name_plural = 'Parts in assembly'
        constraints = [
            models.UniqueConstraint(
                fields=('assembly', 'part'),
                name='unique_part_in_assembly'
            )
        ]
