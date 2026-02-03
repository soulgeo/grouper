from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Like


@receiver(post_save, sender=Like)
def send_notification_on_post_like(sender, instance, created, **kwargs):
    if not created:
        return

    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    group_name = instance.post.user.username
    async_to_sync(channel_layer.group_send)(group_name, {
        'type': 'post_liked',
        'like': instance,
    })
