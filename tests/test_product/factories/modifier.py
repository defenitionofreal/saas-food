import factory

from apps.product.models import Modifier
from tests.test_company.factories import InstitutionFactory


class ModifierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Modifier

    institution = factory.SubFactory(InstitutionFactory)
    title = factory.Faker("word")
