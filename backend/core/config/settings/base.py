"""
Django settings for finargo project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from decouple import config as env_conf
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_conf('DJANGO_KEY')

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # My apps
    'invest.apps.InvestConfig',
    'watchlist.apps.WatchlistConfig',
    'portfolio.apps.PortfolioConfig',
    'notes.apps.NotesConfig',
    'statements.apps.StatementsConfig',
    'news.apps.NewsConfig',
    'analysis.apps.AnalysisConfig',
    'site_admin.apps.AdminConfig',
    # External apps
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Celery
CELERY_BROKER_URL = env_conf('CELERY_BROKER_URL')
CELERY_TASK_TRACK_STARTED = True  # запускает трекинг задач Celery

# Планировщик задач
CELERY_BEAT_SCHEDULER = \
    'django_celery_beat.schedulers:DatabaseScheduler'  # Celery настроен на использование планировщика из базы данных

CELERY_BROKER_TRANSPORT_OPTION = {'visibility_timeout': 3600}  # время ожидания видимости 1 час
CELERY_RESULT_BACKEND = 'django-db'  # указание для django_celery_results куда записывать результат выполнения задач
CELERY_ACCEPT_CONTENT = ['application/json']  # это тип содержимого, разрешенный к получению
CELERY_TASK_SERIALIZER = 'json'  # это строка, используемая для определения метода сериализации по умолчанию
CELERY_RESULT_SERIALIZER = 'json'  # является типом формата сериализации результатов

CELERY_TASK_DEFAULT_QUEUE = 'default'  # celery будет использовать это имя очереди
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Django CORS Headers
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
