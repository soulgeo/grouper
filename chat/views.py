from django.shortcuts import redirect, render

from chat.forms import ChatForm
from chat.models import ChatRoom
from users.models import User, UserProfile


def chat_room(request, room_id):
    print(f'In chat_room view. room_id: {room_id}')
    rooms = ChatRoom.objects.filter(users=request.user)
    selected_room = ChatRoom.objects.get(id=room_id)

    if (
        request.headers.get('HX-Request')
        and request.headers.get('HX-Target') == 'chat_room'
    ):
        template = 'includes/chat_room_container.html'
    else:
        template = 'includes/chat_room.html'

    context = {'rooms': rooms, 'selected_room': selected_room}
    return render(request, template, context)


def chat_home(request):
    user = request.user
    rooms = ChatRoom.objects.with_rich_data(user)  # type: ignore

    active_room = None

    target_user_id = request.GET.get('user_id')
    if target_user_id:
        contact_user = User.objects.get(id=target_user_id)
        active_room, created = ChatRoom.objects.filter(
            chat_type=ChatRoom.ChatType.CONTACTS, users=user
        ).get_or_create(users=contact_user)
        if created:
            room_name = f'{user.username}_{contact_user.username}'
            active_room.name = room_name
            active_room.save()
            active_room.users.set([user, contact_user])

    friend_profiles = UserProfile.objects.filter(
        user__in_contacts_of__user=user
    )

    template = 'chat.html'
    context = {
        'chat_form': ChatForm(),
        'rooms': rooms,
        'active_room': active_room,
        'friend_profiles': friend_profiles,
    }
    return render(request, template, context)


def chat_contact(request, user_id):
    user = request.user
    contact_user = User.objects.get(id=user_id)
    room = (
        ChatRoom.objects.filter(
            chat_type=ChatRoom.ChatType.CONTACTS, users=user
        )
        .filter(users=contact_user)
        .first()
    )

    if not room:
        room = ChatRoom.objects.create(
            chat_type=ChatRoom.ChatType.CONTACTS,
            name=f'{user.username}_{contact_user.username}',
        )
        room.users.set([user, contact_user])

    return redirect('chatroom', room_id=room.id)  # type: ignore


def create_chat_room(request):
    if request.method != 'POST':
        return redirect('/accounts/')

    chat_form = ChatForm(request.POST, request.FILES)
    users = request.POST.getlist('contacts')
    users.append(str(request.user.id))

    if not chat_form.is_valid():
        print('Form errors:', chat_form.errors)
        return redirect('/')

    chat_room_instance = chat_form.save(commit=False)
    chat_room_instance.chat_type = ChatRoom.ChatType.GROUP_CHAT
    chat_room_instance.save()
    chat_room_instance.users.set(users)

    rich_room = ChatRoom.objects.with_rich_data(request.user).get(  # type: ignore
        id=chat_room_instance.id
    )

    context = {
        'room': rich_room,
        'selected_room': rich_room,
        'rooms': ChatRoom.objects.filter(users=request.user),
    }

    return render(request, 'includes/chat_room_container.html', context)
