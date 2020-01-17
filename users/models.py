from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    bio = models.CharField(max_length=300, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True)
    def __str__(self):
        return self.email

    