from .default import *

DEBUG = True
SECRET_KEY = "test"
LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "test.sqlite3"),
    }
}

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
