from django.contrib import admin
from nested_admin.nested import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedTabularInline,
)

from .models import Attachment, Post, PostContent


class AttachmentInline(NestedTabularInline):
    model = Attachment


class PostContentInline(NestedStackedInline):
    model = PostContent
    inlines = [AttachmentInline]


class PostAdmin(NestedModelAdmin):
    inlines = [PostContentInline]


admin.site.register(Post, PostAdmin)
