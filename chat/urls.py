from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<str:room_name>/', views.chat, name='chat'),
    path('messenger/', views.message_index, name='message_index'),
    path('messenger/<str:room_name>/', views.messenger, name='messenger'),
]
