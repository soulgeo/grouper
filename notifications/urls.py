from django.urls import path

from . import views

urlpatterns = [
    path('clear-notification/<int:id>', views.clear_notification, name='clear_notification'),
    path('clear-all-notifications', views.clear_all_notifications, name='clear_all_notifications'),
]
