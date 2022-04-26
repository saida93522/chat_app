"""
ASGI config for chat_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/

To integrate channels,create the routing configuration.
A channel's routing configuration is an asgi application that 
is similar to django configuration in that it tells channel
what code to run when an HTTP request is received by Channel server.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
# from channels.auth import AuthMiddlewareStack
# import chat_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

 # Django's ASGI application to handle traditional HTTP requests

application = get_asgi_application()