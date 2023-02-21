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
