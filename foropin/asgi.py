"""
ASGI config for foropin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foropin.settings')

asgi_application = get_asgi_application() #new

import publication.routing #new

application = ProtocolTypeRouter({
            "http": asgi_application,
            "websocket": URLRouter(publication.routing.websocket_urlpatterns)
                       })
