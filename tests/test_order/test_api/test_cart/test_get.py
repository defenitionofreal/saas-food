from contextlib import suppress
from http import HTTPStatus

from django.test import TestCase

from apps.company.models import Institution
from apps.order.models import Cart
from tests.mixins import ApiTestMixin


class GetCartTestCase(ApiTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.institution = Institution.objects.create(
            user=self.user,
            title="institution",
            domain="domain1",
        )

    def test_get_as_auth(self):
        assert self._user_cart() is None

        self.login_user()
        response = self.api_client.get(
            "/api/order/{0}/customer/cart/".format(self.institution.domain),
        )
        self.user.refresh_from_db()

        assert response.status_code == HTTPStatus.OK
        assert response.data["id"] == self.user.cart_customer.id
        assert self._user_cart()

    def test_get_as_not_auth_twice(self):
        api_url = "/api/order/{0}/customer/cart/".format(self.institution.domain)
        responses = (self.api_client.get(api_url), self.api_client.get(api_url))

        assert Cart.objects.count() == 1
        cart = Cart.objects.first()

        for response in responses:
            assert response.status_code == HTTPStatus.OK
            assert response.data["id"] == cart.id

    def test_after_auth(self):
        api_url = "/api/order/{0}/customer/cart/".format(self.institution.domain)

        response_not_auth = self.api_client.get(api_url)
        assert response_not_auth.status_code == HTTPStatus.OK

        self.login_user()
        assert self._user_cart() is None

        response_auth = self.api_client.get(api_url)
        self.user.refresh_from_db()

        assert response_auth.status_code == HTTPStatus.OK
        assert Cart.objects.count() == 1
        assert self._user_cart()

        response_auth_twice = self.api_client.get(api_url)

        assert response_auth_twice.status_code == HTTPStatus.OK
        assert Cart.objects.count() == 1
        assert self._user_cart()

    def _user_cart(self, user=None):
        with suppress(Exception):
            return (user or self.user).cart_customer
