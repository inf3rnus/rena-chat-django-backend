from rest_framework.serializers import ModelSerializer
from .models import Conversation, Message

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'