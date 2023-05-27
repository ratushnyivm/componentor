import factory
from faker import Factory

from .models import Assembly

factory_en = Factory.create()


class AssemblyFactory(factory.django.DjangoModelFactory):
    designation = factory.Sequence(
        lambda d: f'111.{factory_en.random_number(digits=5)}'
    )
    name = factory.Sequence(lambda n: f'Assembly_{factory_en.word()}{n}')

    class Meta:
        model = Assembly
