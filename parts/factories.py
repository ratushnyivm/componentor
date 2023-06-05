import factory
import materials.factories
from faker import Factory
from parts.models import Part

factory_en = Factory.create()


class PartFactory(factory.django.DjangoModelFactory):

    designation = factory.Sequence(
        lambda d: f'000.{factory_en.random_number(digits=5)}'
    )
    name = factory.Sequence(lambda n: f'Part_{factory_en.word()}{n}')
    material = factory.SubFactory(materials.factories.MaterialFactory)

    class Meta:
        model = Part
