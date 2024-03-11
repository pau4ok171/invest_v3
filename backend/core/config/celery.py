import os
from celery import Celery
from decouple import config as env_conf

# Стандартные настройки для библиотеки Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", env_conf('DJANGO_SETTINGS_MODULE'))

app = Celery('invest')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
