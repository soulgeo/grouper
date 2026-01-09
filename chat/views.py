from django.shortcuts import render

from chat.models import ChatRoom


def chat_room(request, room_id):

    room = ChatRoom.objects.get(id=room_id)
    template = "chat.html"
    context = {"room": room}
    return render(request, template, context)
