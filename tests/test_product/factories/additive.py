import factory
from factory import fuzzy

from apps.product.models import Additive
from tests.test_company.factories import InstitutionFactory
from tests.test_product.factories import CategoryAdditiveFactory


class AdditiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Additive

    institution = factory.SubFactory(InstitutionFactory)
    category = factory.SubFactory(CategoryAdditiveFactory)
    title = factory.Faker("word")
    price = fuzzy.FuzzyDecimal(10, 900, 2)
    is_active = True
