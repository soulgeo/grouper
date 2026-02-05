from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from chat.models import ChatMessage
from core.models import Like
from notifications.models import Notification


@receiver(post_save, sender=Like)
def send_notification_on_post_like(sender, instance, created, **kwargs):
    if not created:
        return

    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    notification = Notification(
        user=instance.post.user,
        message=f"{instance.user.username} liked your post: {instance.post.title}",
        trigger_event=Notification.TriggerEvent.POST_LIKE,
    )
    notification.save()

    group_name = instance.post.user.username
    async_to_sync(channel_layer.group_send)(group_name, {
        'type': 'post_liked',
        'notification': notification,
    })

@receiver(post_save, sender=ChatMessage)
def update_chat_list_on_new_message(sender, instance, created, **kwargs):
    if not created:
        return
    
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    for user in instance.room.users.all():
        async_to_sync(channel_layer.group_send)(
            user.username, {
                "type": "chat.list_update",
                "room_id": instance.room.id,
            }
        )
