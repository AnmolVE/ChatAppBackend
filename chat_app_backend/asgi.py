"""
ASGI config for chat_app_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.route import websocket_urlpatterns
from chat.channels_middleware import JWTAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app_backend.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": application,
    "websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns))
})
