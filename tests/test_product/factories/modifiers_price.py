import factory
from factory import fuzzy

from apps.product.models import ModifierPrice
from tests.test_company.factories import InstitutionFactory
from tests.test_product.factories import ProductFactory, ModifierFactory


class ModifierPriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModifierPrice

    institution = factory.SubFactory(InstitutionFactory)
    product = factory.SubFactory(ProductFactory)
    modifier = factory.SubFactory(ModifierFactory)
    price = fuzzy.FuzzyDecimal(10, 900, 2)
