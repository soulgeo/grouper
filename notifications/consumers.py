from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from django.template.loader import get_template

from chat.models import ChatRoom
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
        notification = event['notification']

        context = {'notification': notification}
        csrf_token = self.scope.get('cookies', {}).get('csrftoken')
        if csrf_token:
            context['csrf_token'] = csrf_token  # type: ignore

        html = get_template('notification_oob.html').render(context=context)
        self.send(text_data=html)

    def chat_list_update(self, event):
        room_id = event['room_id']
        room = ChatRoom.objects.with_rich_data(self.user).get(  # type: ignore
            id=room_id
        )
        print(room.display_profile_image)
        html = get_template('includes/chat_room_card_oob.html').render(
            context={
                'room': room,
                'MEDIA_URL': settings.MEDIA_URL,
            }
        )
        self.send(text_data=html)
