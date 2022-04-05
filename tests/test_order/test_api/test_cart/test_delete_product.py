import pytest

from tests.test_product.factories.product import ProductFactory


@pytest.fixture()
def product(db):
    return ProductFactory.create()


@pytest.fixture()
def cart(product):
    cart = CartFactory.create()


def test_delete_success(api_client, cart, user, product):
    api_client.login_user(user)

    response = api_client.delete("/api/order/{0}/customer/cart/product/{add product id}")

