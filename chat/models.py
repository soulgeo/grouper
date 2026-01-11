from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chat_rooms"
    )

    class ChatType(models.TextChoices):
        CONTACTS = 'Contacts', _('Contacts')
        GROUP_CHAT = 'GroupChat', _('GroupChat')

    chat_type = models.TextField(
        max_length=20, choices=ChatType.choices, default=ChatType.CONTACTS
    )
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return static('src/img/profile_default.png')

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
