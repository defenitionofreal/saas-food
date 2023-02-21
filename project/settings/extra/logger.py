
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
