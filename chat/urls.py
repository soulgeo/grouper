from django.urls import path

from chat import views

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('contact/<int:user_id>', views.chat_contact, name='chat_contact'),
    path('room/', views.create_chat_room, name='create_chat_room'),
    path('room/<int:room_id>', views.chat_room, name='chatroom'),
    path('room/edit/<int:room_id>', views.edit_chat_room, name='edit_chat'),
    path('room/delete/<int:room_id>', views.delete_chat_room, name='delete_chat_room'),
    path('get-rooms/', views.get_user_chat_rooms, name='get_user_chat_rooms'),
]
