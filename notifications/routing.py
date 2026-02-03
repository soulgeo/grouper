from typing import Any, cast

from django.urls import path

from .consumers import NotificationConsumer

websocket_urlpatterns = [
    path("ws/notifications/", cast(Any, NotificationConsumer.as_asgi())),
]
