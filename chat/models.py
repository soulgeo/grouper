from django.conf import settings
from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chat_rooms"
    )

    def __str__(self) -> str:
        return self.name


class ChatMessage(models.Model):
    room = models.ForeignKey(
        ChatRoom, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="chat_messages",
        on_delete=models.CASCADE,
    )
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.author}: {self.body}"

    class Meta:
        ordering = ["-created_at"]
