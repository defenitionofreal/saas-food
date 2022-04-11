from contextlib import suppress
from http import HTTPStatus

import pytest

from apps.order.models import Cart
from tests.test_company.factories import InstitutionFactory


@pytest.fixture()
def institution(user):
    return InstitutionFactory.create(user=user)


def test_get_as_auth(institution, user, api_client):
    assert _user_cart(user) is None

    api_client.login_user(user)
    response = api_client.get(
        "/api/order/{0}/customer/cart/".format(institution.domain),
    )
    user.refresh_from_db()

    assert response.status_code == HTTPStatus.OK
    assert response.data["id"] == user.cart_customer.id
    assert _user_cart(user)


def test_get_as_not_auth_twice(institution, user, api_client):
    api_url = "/api/order/{0}/customer/cart/".format(institution.domain)
    responses = (api_client.get(api_url), api_client.get(api_url))

    assert Cart.objects.count() == 1
    cart = Cart.objects.first()

    for response in responses:
        assert response.status_code == HTTPStatus.OK
        assert response.data["id"] == cart.id


def test_after_auth(institution, user, api_client):
    api_url = "/api/order/{0}/customer/cart/".format(institution.domain)

    response_not_auth = api_client.get(api_url)
    assert response_not_auth.status_code == HTTPStatus.OK

    api_client.login_user(user)
    assert _user_cart(user) is None

    response_auth = api_client.get(api_url)
    user.refresh_from_db()

    assert response_auth.status_code == HTTPStatus.OK
    assert Cart.objects.count() == 1
    assert _user_cart(user)

    response_auth_twice = api_client.get(api_url)

    assert response_auth_twice.status_code == HTTPStatus.OK
    assert Cart.objects.count() == 1
    assert _user_cart(user)


def _user_cart(user):
    with suppress(Exception):
        return user.cart_customer
