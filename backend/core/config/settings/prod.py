from .base import *
import os

URL_PREFIX = 'https://finargo.ru'

DEBUG = False

ADMINS = [
    ('Pavel M', 'finargo@mail.ru'),
]

SITE_ID = 1

ALLOWED_HOSTS = ['www.finargo.ru', 'finargo.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Безопасность
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
