"""
WSGI config for finargo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from decouple import config as env_conf
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_conf('DJANGO_SETTINGS_MODULE'))

application = get_wsgi_application()
