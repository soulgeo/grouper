from django.conf import settings
from django.db import models
from django.db.models import Case, CharField, F, OuterRef, Subquery, Value, When
from django.db.models.functions import Concat
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _


class ChatRoomQuerySet(models.QuerySet):
    def with_rich_data(self, user):
        from users.models import UserProfile
        
        latest_message = (
            ChatMessage.objects.filter(
                room=OuterRef('pk'),
            )
            .annotate(
                message_str=Concat(
                    Value('@'),
                    F('author__username'),
                    Value(': '),
                    F('body'),
                    output_field=CharField(),
                )
            )
            .order_by('-created_at')
        )

        profile_qs = UserProfile.objects.filter(
            user__chat_rooms=OuterRef('pk')
        ).exclude(user=user)

        return self.annotate(
            latest_message=Subquery(latest_message.values('message_str')[:1]),
            latest_message_at=Subquery(latest_message.values('created_at')[:1]),
        ).annotate(
            display_profile_image=Case(
                When(
                    chat_type=ChatRoom.ChatType.CONTACTS,
                    then=Subquery(profile_qs.values('image')[:1]),
                ),
                default=Value(None),
                output_field=CharField(),
            ),
            display_full_name=Case(
                When(
                    chat_type=ChatRoom.ChatType.CONTACTS,
                    then=Subquery(
                        profile_qs.annotate(
                            full_name=Concat(
                                'user__first_name',
                                Value(' '),
                                'user__last_name',
                            )
                        ).values('full_name')[:1]
                    ),
                ),
                default=Value(None),
                output_field=CharField(),
            ),
        ).annotate(
            display_name=Case(
                When(chat_type=ChatRoom.ChatType.GROUP_CHAT, then=F('name')),
                default=F('display_full_name'),
                output_field=CharField(),
            )
        ).order_by(F('latest_message_at').desc(nulls_last=True))


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

    objects = ChatRoomQuerySet.as_manager()

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        if self.chat_type == self.ChatType.GROUP_CHAT:
            return static('src/img/group_default.png')
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
        return f"@{self.author.username}: {self.body}"

    class Meta:
        ordering = ["-created_at"]
