from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template

from notifications.models import Notification


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']  # type: ignore
        if not self.user:
            return

        self.group_name = self.user.username
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code: int) -> None:
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
        return super().disconnect(code)

    def post_liked(self, event):
        like = event['like']
        notification = Notification(
            user=self.user,
            message=f"{like.user.username} liked your post: {like.post.title}",
            trigger_event=Notification.TriggerEvent.POST_LIKE,
        )
        notification.save()

        html = get_template('notification_oob.html').render(
            context={
                'notification': notification,
            }
        )
        self.send(text_data=html)
