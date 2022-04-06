import factory

from apps.order.models import Cart
from tests.test_company.factories import InstitutionFactory


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    institution = factory.SubFactory(InstitutionFactory)
