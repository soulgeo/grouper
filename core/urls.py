from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts', views.contacts, name='contacts'),
    path('secret/', views.secret, name='secret'),
]
