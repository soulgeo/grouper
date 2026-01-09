from django.urls import path

from chat import views

urlpatterns = [path('room/<int:room_id>', views.chat_room, name='chatroom')]
