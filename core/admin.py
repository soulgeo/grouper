from django.contrib import admin
from nested_admin.nested import (
    NestedModelAdmin,
    NestedStackedInline,
    NestedTabularInline,
)

from .models import Attachment, Contact, Post, PostContent


class AttachmentInline(NestedTabularInline):
    model = Attachment


class PostContentInline(NestedStackedInline):
    model = PostContent
    inlines = [AttachmentInline]


class PostAdmin(NestedModelAdmin):
    inlines = [PostContentInline]


class ContactAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not Contact.objects.filter(
            user=obj.contact, contact=obj.user
        ).exists():
            Contact.objects.create(user=obj.contact, contact=obj.user)

    def delete_model(self, request, obj):
        Contact.objects.filter(user=obj.contact, contact=obj.user).delete()
        super().delete_model(request, obj)


admin.site.register(Post, PostAdmin)
admin.site.register(Contact, ContactAdmin)
