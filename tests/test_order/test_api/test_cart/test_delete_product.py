from http import HTTPStatus

import pytest

from tests.test_order.factories import CartFactory, CartProductFactory


@pytest.fixture()
def cart(user):
    cart = CartFactory.create(customer=user)
    CartProductFactory.create(cart=cart)

    return cart


def test_delete_success(api_client, cart, user):
    assert cart.cart_products.count() == 1

    api_client.login_user(user)

    response = api_client.delete(
        "/api/order/{0}/customer/cart/product/".format(cart.institution.domain),
        data={"cart_product": cart.cart_products.first().id},
    )

    cart.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert response.data["id"] == cart.id
    assert not cart.cart_products.exists()


def test_delete_not_exists(api_client, cart, user):
    assert cart.cart_products.count() == 1

    api_client.login_user(user)

    response = api_client.delete(
        "/api/order/{0}/customer/cart/product/".format(cart.institution.domain),
        data={"cart_product": 0},
    )

    cart.refresh_from_db()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert cart.cart_products.count() == 1
