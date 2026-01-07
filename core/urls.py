from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('p/<str:username>/', views.profile, name='profile'),
    path('profileedit', views.edit_profile, name='edit_profile'),
    path('search/', views.search_posts, name='search'),
    path('contacts/', views.contacts, name='contacts'),
    path('submit-post', views.create_post, name='submit_post'),
    path('like-post/<int:post_id>', views.like_post, name='like_post'),
    path(
        'send-friend-request/<str:username>',
        views.send_friend_request,
        name='send-friend-request',
    ),
    path('friend-requests', views.friend_requests, name='friend_requests'),
    path(
        'accept-friend-request/<int:id>',
        views.accept_friend_request,
        name='accept_friend_request',
    ),
    path('search-users', views.search_users, name='search_users'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('edit-post/<int:post_id>', views.edit_post, name='edit_post'),
]
