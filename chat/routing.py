from typing import Any, cast

from django.urls import path

from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("ws/chatroom/<room_id>", cast(Any, ChatConsumer.as_asgi())),
]
