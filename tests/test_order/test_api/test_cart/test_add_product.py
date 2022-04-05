from http import HTTPStatus

from django.test import TestCase

from apps.company.models import Institution
from apps.product.models.enums import WeightUnit
from tests.mixins import ApiTestMixin
from apps.product.models import Product, Category


class GetCartTestCase(ApiTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.institution = Institution.objects.create(
            user=self.user,
            title="institution",
            domain="domain1",
        )

        product_category_kwargs = {"institution": self.institution, "is_active": True}
        pizza = Category.objects.create(title="Pizza", slug="pizza", **product_category_kwargs)
        drinks = Category.objects.create(title="Drink", slug="drinks", **product_category_kwargs)

        self.product1 = Product.objects.create(
            category=pizza,
            title="Margarita",
            description="Margarita",
            price=450,
            weight_unit=WeightUnit.GRAM,
            weight=400,
            cook_time=40,
            slug="margarita",
            **product_category_kwargs,
        )
        self.product2 = Product.objects.create(
            category=drinks,
            title="Coca cola",
            description="Coca cola",
            price=95,
            weight_unit=WeightUnit.MILLILITER,
            weight=300,
            cook_time=3,
            slug="coca-cola",
            **product_category_kwargs,
        )

    def test_add_product(self):
        """Test add product to cart."""
        product_data = {
            "product": self.product1.id,
            "modifiers": [],
            "additives": [],
            "quantity": 2,
        }

        self.login_user()
        response = self.api_client.post(
            "/api/order/{0}/customer/cart/add/".format(self.institution.domain),
            data=product_data,
            format="json",
        )
        self.user.refresh_from_db()

        assert response.status_code == HTTPStatus.OK
        assert self.user.cart_customer.cart_products.count() == 1

        cart_product = self.user.cart_customer.cart_products.first()

        assert cart_product.product == self.product1
        assert cart_product.quantity == 2
        assert not cart_product.modifiers.exists()
        assert not cart_product.additives.exists()

    def test_add_product_modifier(self):
        raise NotImplementedError()

    def test_add_product_addative(self):
        raise NotImplementedError()

    def test_add_product_modifier_and_addative(self):
        raise NotImplementedError()

    def test_merge_products(self):
        raise NotImplementedError()
