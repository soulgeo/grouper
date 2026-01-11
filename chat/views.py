from django.db.models import Case, CharField, F, OuterRef, Subquery, Value, When
from django.db.models.functions import Concat
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
            room=OuterRef('pk'),
        )
        .order_by('-created_at')
        .values('created_at')[:1]
    )

    profile_qs = UserProfile.objects.filter(
        user__chat_rooms=OuterRef('pk')
    ).exclude(user=user)

    rooms = (
        ChatRoom.objects.filter(users=user)
        .annotate(latest_message_at=Subquery(latest_message))
        .annotate(
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
        )
        .annotate(
            display_name=Case(
                When(chat_type=ChatRoom.ChatType.GROUP_CHAT, then=F('name')),
                default=F('display_full_name'),
                output_field=CharField(),
            )
        )
        .order_by(F('latest_message_at').desc(nulls_last=True))
    )

    active_room = None

    target_user_id = request.GET.get('user_id')
    if target_user_id:
        contact_user = User.objects.get(id=target_user_id)
        active_room, created = ChatRoom.objects.filter(
            chat_type=ChatRoom.ChatType.CONTACTS, users=user
        ).get_or_create(users=contact_user)
        if created:
            room_name = f"{user.username}_{contact_user.username}"
            active_room.name = room_name
            active_room.save()
            active_room.users.set(user + contact_user)

    template = 'chat.html'
    context = {'rooms': rooms, 'active_room': active_room}
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
