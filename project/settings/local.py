from .default import *

DEBUG = eval(os.environ.get('DEBUG', 'True'))

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'food',
#         'USER': 'food',
#         'PASSWORD': 'food',
#         'HOST': '',
#         'PORT': 5432,
#     }
# }
