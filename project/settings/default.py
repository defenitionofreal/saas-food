from sys import path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket
from datetime import timedelta

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(PROJECT_DIR)

FIXTURE_DIRS = (
   os.path.join(PROJECT_DIR, 'fixtures'),
)

PROJECT_ROOT = os.path.dirname(BASE_DIR)

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG')

INTERNAL_IPS = ["172.18.0.1"]
# if DEBUG:
#     hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
#     INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1",
#                                                                  "10.0.2.2",
#                                                                  "192.168.48.1"]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',  # important one
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

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
    'apps.company',
    'apps.delivery',
    'apps.location',
    'apps.media',
    'apps.order',
    'apps.payment',
    'apps.plan',
    'apps.product',
    'apps.que',
    # devide clients
    'apps.customer',
    'apps.organization',
]

INSTALLED_APPS = CORE_APPS + THIRD_PART_APPS + INTERNAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # corsheaders
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',  # toolbar
    'debug_toolbar_force.middleware.ForceDebugToolbarMiddleware', # ?debug-toolbar
    # custom
    'apps.base.middleware.MoveJWTRefreshCookieIntoTheBody'
]

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

# send emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
#EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
#DEFAULT_FROM_EMAIL = 'No reply <noreply@mail.ru>'
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PHONENUMBER_DEFAULT_REGION = 'RU'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=90),
}

# https://pypi.org/project/django-cors-headers/
CORS_ALLOW_CREDENTIALS = True  # to accept cookies via ajax request
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:4000',
    'http://localhost:8080',
    'http://localhost:8000',
    'http://localhost',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:4000',
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://127.0.0.1',
    'https://example-frontend.com',
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

AUTH_USER_MODEL = 'base.CustomUser'

SITE_ID = 1

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER')
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_BROKER_CONNECTION_TIMEOUT = 20
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BACKEND')
# CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# SESSIONS
CART_SESSION_ID = 'cart_id'
DELIVERY_SESSION_ID = 'delivery_id'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  #.cache
# 2 weeks
SESSION_COOKIE_AGE = 12000 #60 * 60 * 24 * 7 * 2
# if window closed session still live
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console', ],
        # },
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

# Authentication
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend",
                           "apps.base.backends.AuthBackend"]

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
