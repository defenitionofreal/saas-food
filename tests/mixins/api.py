from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.base.authentication import JWTAuthentication

TEST_USER_PHONE = "89004003020"
TEST_USER_PASSWORD = "AaBbCc1234"

User = get_user_model()


class ApiTestMixin:
    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.create(phone=TEST_USER_PHONE)
        self.user.set_password(TEST_USER_PASSWORD)
        self.user.save()

        self.api_client = APIClient(defaults={"content_type": "application/json"})

    def login_user(self, user=None) -> None:
        user = user or self.user
        self.api_client.cookies.load({"jwt": JWTAuthentication.generate_jwt(user.id, scope="")})

    def logout(self):
        self.api_client.cookies.load({"jwt": None})
