from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default = True
    name = 'notifications'

    def ready(self):
        from . import signals
