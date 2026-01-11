from django.db.models import F, OuterRef, Subquery
from django.shortcuts import redirect, render

from chat.models import ChatMessage, ChatRoom
from users.models import User, UserProfile


def chat_room(request, room_id):
    room = ChatRoom.objects.get(id=room_id)
    partial = 'includes/chat_room.html'
    context = {'room': room}
    return render(request, partial, context)


def chat_home(request):
    user = request.user

    latest_message = (
        ChatMessage.objects.filter(
            room__chat_type=ChatRoom.ChatType.CONTACTS,
            room__users=user,
        )
        .filter(room__users=OuterRef('user'))
        .order_by('-created_at')
        .values('created_at')[:1]
    )

    profiles = (
        UserProfile.objects.filter(user__in_contacts_of__user=user)
        .annotate(latest_message_at=Subquery(latest_message))
        .order_by(F('latest_message_at').desc(nulls_last=True))
    )

    room = None

    target_user_id = request.GET.get('user_id')
    if target_user_id:
        contact_user = [User.objects.get(id=target_user_id)]
        user = [user]
        room, created = ChatRoom.objects.filter(
            chat_type=ChatRoom.ChatType.CONTACTS, users__in=user
        ).get_or_create(users__in=contact_user)
        if created:
            room_name = f"{user[0].username}_{contact_user[0].username}"
            room.name = room_name
            room.save()
            room.users.set(user + contact_user)

    template = 'chat.html'
    context = {'profiles': profiles, 'room': room}
    return render(request, template, context)


def chat_contact(request, user_id):
    user = [request.user]
    contact_user = [User.objects.get(id=user_id)]
    room, created = ChatRoom.objects.filter(
        chat_type=ChatRoom.ChatType.CONTACTS, users__in=user
    ).get_or_create(users__in=contact_user)
    if created:
        room_name = f"{user[0].username}_{contact_user[0].username}"
        room.name = room_name
        room.save()
        room.users.set(user + contact_user)

    return redirect('chatroom', room_id=room.id)  # type: ignore
