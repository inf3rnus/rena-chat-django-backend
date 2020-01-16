from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('pk', 'email', 'username', 'bio', 'profile_picture')