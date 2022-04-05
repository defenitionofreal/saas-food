import factory

from apps.product.models import Category
from tests.test_company.factories import InstitutionFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    institution = factory.SubFactory(InstitutionFactory)
    is_active = True
    title = factory.Faker("word")
    slug = factory.Faker("word")
