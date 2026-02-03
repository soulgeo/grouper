from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


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
        message = f"{like.user.username} liked your post: {like.post.title}"
        self.send(text_data=message)
