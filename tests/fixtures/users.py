import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

USER_EMAIL = "user-test@mail.com"
USERNAME = "user"
USER_PASSWORD = "123456789Abc"
HASHED_PASSWORD = make_password(USER_PASSWORD)


@pytest.fixture()
def user(db):
    user, _ = User.objects.get_or_create(
        email=USER_EMAIL,
        defaults={
            "username": USERNAME,
            "first_name": "First",
            "last_name": "Last",
            "password": HASHED_PASSWORD,
        },
    )
    return user
