"""
ASGI config for finargo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from decouple import config as env_conf
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_conf('DJANGO_SETTINGS_MODULE'))

django_asgi_app = get_asgi_application()

# Импортируем consumers ПОСЛЕ инициализации Django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path, re_path
from . import consumers

application = ProtocolTypeRouter({
    'http': ASGIStaticFilesHandler(django_asgi_app),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/api/v1/prices', consumers.PriceConsumer.as_asgi()),
            re_path(r'^ws/api/v1/prices/(?P<company_slug>[\w-]+)/$', consumers.CompanyDetailPriceConsumer.as_asgi()),
        ])
    ),
})
