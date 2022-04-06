import factory

from apps.order.models import CartProduct
from tests.test_order.factories import CartFactory
from tests.test_product.factories import ProductFactory


class CartProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartProduct

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)

    @factory.post_generation
    def modifiers(self, create, extracted, **kwargs):
        if create and extracted:
            self.modifiers.set(extracted)

    @factory.post_generation
    def additives(self, create, extracted, **kwargs):
        if create and extracted:
            self.additives.set(extracted)
