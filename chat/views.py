from django.shortcuts import redirect, render

from chat.models import ChatRoom
from users.models import User, UserProfile


def chat_room(request, room_id):
    room = ChatRoom.objects.get(id=room_id)
    partial = 'includes/chat_room.html'
    context = {'room': room}
    return render(request, partial, context)


def chat_home(request):
    user = request.user
    profiles = UserProfile.objects.filter(user__in_contacts_of__user=user)

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
