import factory

from apps.company.models import Institution
from tests.test_base.factories import UserFactory


class InstitutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Institution

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("word")
    domain = factory.Faker("word")
