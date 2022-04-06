import pytest
from rest_framework.test import APIClient as BaseAPIClient

from apps.base.authentication import JWTAuthentication


class APIClient(BaseAPIClient):
    def login_user(self, user) -> None:
        self.cookies.load({"jwt": JWTAuthentication.generate_jwt(user.id, scope="")})

    def logout_user(self):
        self.cookies.load({"jwt": None})


@pytest.fixture()
def api_client(db) -> APIClient:
    return APIClient(
        defaults={"content_type": "application/json", "format": "json"},
    )
