import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from users.models import UserProfile

from .models import ChatMessage, ChatRoom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']  # type: ignore
        self.room_id = self.scope['url_route']['kwargs']['room_id']  # type: ignore

        self.chatroom = get_object_or_404(ChatRoom, id=self.room_id)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom.name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom.name, self.channel_name
        )
        return super().disconnect(code)

    def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return super().receive(text_data, bytes_data)

        text_data_json = json.loads(text_data)
        body = text_data_json['body']

        message = ChatMessage.objects.create(
            body=body, author=self.user, room=self.chatroom
        )

        async_to_sync(self.channel_layer.group_send)(
            self.chatroom.name,
            {'type': 'chat.message', 'message': message},
        )

    def chat_message(self, event):
        message = event['message']
        
        self.chatroom.latest_message = message  # type: ignore

        if self.chatroom.chat_type == ChatRoom.ChatType.GROUP_CHAT:
            self.chatroom.display_name = self.chatroom.name  # type: ignore
        else:
            other_profile = (
                UserProfile.objects.filter(user__chat_rooms=self.chatroom)
                .exclude(user=self.user)
                .first()
            )
            if other_profile:
                self.chatroom.display_name = (  # type: ignore
                    f'{other_profile.user.first_name} {other_profile.user.last_name}'
                )
                self.chatroom.display_profile_image = (  # type: ignore
                    other_profile.image.url if other_profile.image else None
                )
            else:
                self.chatroom.display_name = 'Unknown'  # type: ignore
                self.chatroom.display_profile_image = None  # type: ignore

        html = get_template('includes/chat_message_oob.html').render(
            context={
                'message': message,
                'user': self.user,
                'room': self.chatroom,
            }
        )
        self.send(text_data=html)
