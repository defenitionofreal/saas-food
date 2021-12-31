from .default import *

DEBUG = os.environ['DJANGO_DEBUG']

# USE_X_FORWARDED_HOST = True
# USE_X_FORWARDED_PORT = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'food'),
        'USER': os.environ.get('POSTGRES_USER', 'food'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'food'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.environ['CELERY_BROKER_URL']],
        },
    },
}
