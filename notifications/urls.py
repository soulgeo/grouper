from django.urls import path

from . import views

urlpatterns = [
    path('clear-notifications', views.clear_notifications, name='clear_notifications'),
]
