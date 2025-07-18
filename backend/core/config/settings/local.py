from .base import *

URL_PREFIX = 'http://127.0.0.1:8000'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 2

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
