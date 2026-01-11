from django.urls import path

from chat import views

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('contact/<int:user_id>', views.chat_contact, name='chat_contact'),
    path('room/<int:room_id>', views.chat_room, name='chatroom'),
]
