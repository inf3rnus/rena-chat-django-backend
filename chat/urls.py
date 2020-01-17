# chat/urls.py
from django.urls import include, path
from .views import get_conversation_messages

urlpatterns = [
    path('get_conversation_messages/', get_conversation_messages)
]