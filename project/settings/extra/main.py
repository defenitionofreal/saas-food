from sys import path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')
#
# INTERNAL_IPS = ["172.18.0.1"]
# if DEBUG:
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1",
#                                                                  "10.0.2.2",
#                                                                  "192.168.48.1"]

ALLOWED_HOSTS = ['*', ]

# Application definition
CORE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'debug_toolbar',

    'django.contrib.sites',
]

THIRD_PART_APPS = [
    'rest_framework',
    #'rest_framework.authtoken',
    'corsheaders',  # https://github.com/adamchainz/django-cors-headers
    'phonenumber_field',
    'drf_yasg',
    'django_celery_beat',
    'django_celery_results',
    'django_cleanup',
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]

INTERNAL_APPS = [
    'apps.base',
    'apps.authentication',
    'apps.notification',
    'apps.company',
    'apps.delivery',
    'apps.media',
    'apps.order',
    'apps.payment',
    'apps.plan',
    'apps.product',
    'apps.que',
    'apps.mail',
    'apps.sms',

    # separate users
    'apps.customer',
    'apps.organization',
]

INSTALLED_APPS = CORE_APPS + THIRD_PART_APPS + INTERNAL_APPS
ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', default='food'),
        'USER': os.environ.get('POSTGRES_USER', default='food'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default='food'),
        'HOST': os.environ.get('POSTGRES_HOST', default='localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', default=5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'  # or UTC?

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

PHONENUMBER_DEFAULT_REGION = 'RU'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

AUTH_USER_MODEL = 'base.CustomUser'

SITE_ID = 1

# SESSIONS
CART_SESSION_ID = 'cart_id'
DELIVERY_SESSION_ID = 'delivery_id'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  #.cache
# 2 weeks
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# if window closed session still live
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False

# Authentication
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

AUTHENTICATION_CODE_EXPIRED = 5 * 60
AUTHENTICATION_SEND_CODE_WINDOW = 30
AUTHENTICATION_PHONE_NUMBERS_COUNT_FROM_IP = 10
AUTHENTICATION_PHONE_NUMBERS_EXPIRED_FROM_IP = 10 * 60
MAX_GENERATE_ATTEMPTS_COUNT = 100

# SMS AERO API
SMS_AERO_API_URL = os.environ.get('SMS_AERO_API_URL')
SMS_AERO_API_EMAIL = os.environ.get('SMS_AERO_API_EMAIL')
SMS_AERO_API_KEY = os.environ.get('SMS_AERO_API_KEY')

# чтобы зарегать свою подпись вместо SMS Aero
# нужно оставить заявку
SMS_AERO_API_SIGN = "SMS Aero"

STRIPE_SK = os.environ.get("STRIPE_SK")
