import factory
from factory import fuzzy

from apps.product.models import Product
from apps.product.models.enums import WeightUnit
from tests.test_company.factories import InstitutionFactory
from tests.test_product.factories import CategoryFactory


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    institution = factory.SubFactory(InstitutionFactory)
    is_active = True
    category = factory.SubFactory(CategoryFactory)
    title = factory.Faker("word")
    description = factory.Faker("word")
    price = fuzzy.FuzzyDecimal(10, 900, 2)
    weight_unit = WeightUnit.GRAM
    weight = fuzzy.FuzzyFloat(100, 600)
    cook_time = fuzzy.FuzzyInteger(3, 59)
    slug = factory.Faker("word")
