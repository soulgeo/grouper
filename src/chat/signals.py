from django.dispatch import receiver
from chat.models import ChatRoom
from core.models import Contact
from core.signals import contact_created

@receiver(contact_created, sender=Contact)
def create_chat_room_on_contact_created(sender, instance, **kwargs):
    user1 = instance.user
    user2 = instance.contact
    
    room = (
        ChatRoom.objects.filter(
            chat_type=ChatRoom.ChatType.CONTACTS, users=user1
        )
        .filter(users=user2)
        .first()
    )

    if not room:
        room = ChatRoom.objects.create(
            chat_type=ChatRoom.ChatType.CONTACTS,
            name=f'{user1.username}_{user2.username}',
        )
        room.users.set([user1, user2])
