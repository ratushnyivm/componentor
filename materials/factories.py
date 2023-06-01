import factory
from faker import Factory
from materials.models import Material

factory_en = Factory.create()


class MaterialFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda n: f'Material_{factory_en.word()}{n}')
    density = factory.Sequence(lambda d: factory_en.random_number(digits=5))

    class Meta:
        model = Material
