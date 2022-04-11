import factory

from apps.product.models import CategoryAdditive
from tests.test_company.factories import InstitutionFactory


class CategoryAdditiveFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryAdditive

    institution = factory.SubFactory(InstitutionFactory)
    title = factory.Faker("word")
    is_active = True
