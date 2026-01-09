import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

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
            {"type": "chat.message", "message": message},
        )

    def chat_message(self, event):
        message = event["message"]
        html = get_template('includes/chat_message_p.html').render(
            context={'message': message, 'user': self.user}
        )
        self.send(text_data=html)
