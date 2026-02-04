from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class TriggerEvent(models.TextChoices):
        POST_LIKE = 'PostLike', _('PostLike')
        POST_COMMENT = 'PostComment', _('PostComment')

    trigger_event = models.CharField(
        max_length=15, choices=TriggerEvent.choices, blank=True
    )
