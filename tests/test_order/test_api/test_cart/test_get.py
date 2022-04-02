# TODO: Implement factory boy, pytests for dev-development

from django.test import TestCase
from apps.company.models import Institution
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from apps.base.authentication import JWTAuthentication
from http.cookies import SimpleCookie
from http import HTTPStatus

TEST_USER_PASSWORD = "AaBbCc1234"

User = get_user_model()


class GetCartTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(phone="89004003020")
        cls.user.set_password(TEST_USER_PASSWORD)
        cls.user.save()

        cls.client = APIClient(defaults={"content_type": "application/json"})
        # cls.client.cookies.load({"jwt": JWTAuthentication.generate_jwt(cls.user.id, scope="")})

    def setUp(self):
        self.institution = Institution.objects.create(
            user=self.user,
            title="institution",
            domain="domain1",
        )

    def test_get_as_auth(self):
        # headers = {"jwt": JWTAuthentication.generate_jwt(self.user.id, scope="")}

        session = self.client.session
        session["jwt"] = JWTAuthentication.generate_jwt(self.user.id, scope="")
        session.save()

        response = self.client.get(
            "/api/order/{0}/customer/cart/".format(self.institution.domain),
        )

        assert response.status_code == HTTPStatus.OK

