import factory
from factory import fuzzy

from apps.product.models import Additive
from tests.test_company.factories import InstitutionFactory


class AdditiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Additive

    institution = factory.SubFactory(InstitutionFactory)
    title = factory.Faker("word")
    price = fuzzy.FuzzyDecimal(10, 900, 2)
    is_active = True
