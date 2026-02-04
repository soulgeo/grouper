from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from chat.forms import ChatForm
from chat.models import ChatRoom
from users.models import User, UserProfile


def chat_room(request, room_id):
    rooms = ChatRoom.objects.filter(users=request.user).distinct()
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
    rooms = ChatRoom.objects.filter(users=user).distinct().with_rich_data(user)  # type: ignore

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
    if not chat_room_instance.image and 'image' in request.FILES:
        chat_room_instance.image = request.FILES['image']
    chat_room_instance.save()
    chat_room_instance.users.set(users)

    rich_room = ChatRoom.objects.with_rich_data(request.user).get(  # type: ignore
        id=chat_room_instance.id
    )

    context = {
        'room': rich_room,
        'selected_room': rich_room,
        'rooms': ChatRoom.objects.filter(users=request.user).distinct(),
    }

    return render(request, 'includes/chat_room_container.html', context)


def edit_chat_room(request, room_id):
    print(f"DEBUG: edit_chat_room called for room {room_id}")
    room = get_object_or_404(ChatRoom, id=room_id)

    if not room.users.filter(id=request.user.id).exists():
        return HttpResponse("Unauthorized", status=403)

    if request.method == "GET":
        chat_form = ChatForm(instance=room)
        selected_profiles = list(room.users.values_list('id', flat=True))

        friend_profiles = UserProfile.objects.filter(
            user__in_contacts_of__user=request.user
        )

        context = {
            'room': room,
            'chat_form': chat_form,
            'selected_profiles': selected_profiles,
            'friend_profiles': friend_profiles,
            'modal_id': f'edit_modal_{room_id}',
            'form_title': 'Edit Chat Room',
            'submit_text': 'Edit',
            'chat_url': reverse('edit_chat', args=[room_id]),
            'hx_target': f'#room-{room_id}',
            'hx_swap': 'outerHTML',
            'hide_trigger': True,
            'auto_open': True,
        }
        
        return render(request, 'includes/chat_form.html', context)

    if request.method != "POST":
        return redirect('/accounts')  # TODO: Change Redirect

    chat_form = ChatForm(request.POST, request.FILES, instance=room)
    if not chat_form.is_valid():
        print('Form errors:', chat_form.errors)
        return redirect('/')  # TODO: Error

    users = request.POST.getlist('contacts') + [request.user]
    chat_room_instance = chat_form.save(commit=False)
    chat_room_instance.save()
    chat_room_instance.users.set(users)

    rich_room = ChatRoom.objects.with_rich_data(request.user).get(  # type: ignore
        id=chat_room_instance.id
    )

    context = {
        'room': rich_room,
        'selected_room': rich_room,
        'rooms': ChatRoom.objects.filter(users=request.user).distinct(),
    }

    return render(request, 'includes/chat_room_edit_oob.html', context)
