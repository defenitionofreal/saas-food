from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.company.models import Institution
from tests.mixins import ApiTestMixin

TEST_USER_PASSWORD = "AaBbCc1234"

User = get_user_model()


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

    def _user_cart(self, user=None):
        user = user or self.user
        try:
            return user.cart_customer
        except Exception:
            return None
