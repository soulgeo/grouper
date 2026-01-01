from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('p/<str:username>/', views.profile, name='profile'),
    path('profileedit', views.edit_profile, name='edit_profile'),
    path('search/', views.search_post, name='search'),
    path('contacts/', views.contacts, name='contacts'),
    path('submit-post', views.create_post, name='submit-post'),
    path('like-post/<int:post_id>', views.like_post, name='like-post'),
]
