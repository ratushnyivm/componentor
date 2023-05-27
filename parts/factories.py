import factory
from faker import Factory
from materials import factories

from .models import Part

factory_en = Factory.create()


class PartFactory(factory.django.DjangoModelFactory):

    designation = factory.Sequence(
        lambda d: f'000.{factory_en.random_number(digits=5)}'
    )
    name = factory.Sequence(lambda n: f'Part_{factory_en.word()}{n}')
    material = factory.SubFactory(factories.MaterialFactory)

    class Meta:
        model = Part
