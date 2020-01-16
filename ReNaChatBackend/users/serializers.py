from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from . import models
from .models import Friend

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('pk', 'email', 'username', 'bio', 'profile_picture')