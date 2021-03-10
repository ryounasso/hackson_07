"""
ASGI config for hackson_07 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

# from channels.routing import URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter
# import os
# import chat.routing
# import django

# from django.core.asgi import get_asgi_application
# from channels.routing import get_default_application

# django.setup()

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackson_07.settings')

# # application = get_default_application()

# # application = get_asgi_application()
# django_asgi_app = get_asgi_application()


# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
# })


# from channels.routing import URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter
# import os
# import chat.routing

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackson_07.settings')


# #application = get_asgi_application()
# django_asgi_app = get_asgi_application()


# application = ProtocolTypeRouter({
#     'http': django_asgi_app,
#     'websocket': AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
# })

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
application = get_default_application()
