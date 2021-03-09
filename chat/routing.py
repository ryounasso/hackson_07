from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('wss://chat/', consumers.ChatConsumer.as_asgi()),
]
