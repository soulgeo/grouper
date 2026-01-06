from typing import TYPE_CHECKING

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='in_contacts_of',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        unique_together = ('user', 'contact')

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.contact.username}"


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_friend_requests',
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_friend_requests',
        on_delete=models.CASCADE,
    )

    class Status(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        ACCEPTED = 'Accepted', _('Accepted')
        REJECTED = 'Rejected', _('Rejected')

    status = models.TextField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Friend request: {self.sender.username} -> {self.receiver.username}"


class InterestCategory(models.Model):
    name = models.CharField(max_length=100)


class Interest(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        InterestCategory, on_delete=models.CASCADE, related_name="interests"
    )

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    if TYPE_CHECKING:
        id: int
        content: 'PostContent'

    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE
    )

    class Visibility(models.TextChoices):
        PUBLIC = "Public", _("Public")
        CONTACTS_ONLY = "Contacts Only", _("Contacts Only")

    visibility = models.CharField(
        max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC
    )

    interests = models.ManyToManyField(Interest, related_name="posts")

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likes"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self) -> str:
        return f"{self.title}, by {self.user}, {self.created_at}"


class PostContent(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, related_name='content'
    )
    text = models.TextField(max_length=500)


class Attachment(models.Model):
    class AttachmentType(models.TextChoices):
        PHOTO = "Photo", _("Photo")
        VIDEO = "Video", _("Video")

    file = models.FileField('Attachment', upload_to='attachments/')
    file_type = models.CharField(
        'File type', choices=AttachmentType.choices, max_length=10
    )

    publication = models.ForeignKey(PostContent, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Attachment'
        verbose_name_plural = 'Attachments'
