from django.db import models
from users.models import CustomUser

# Create your models here.
class Conversation(models.Model):
    users = models.ManyToManyField(CustomUser, related_name='conversation_users')

class Message(models.Model):
    user_profile = models.ForeignKey(CustomUser, related_name='message_user', on_delete=models.CASCADE, null=True)
    conversation = models.ForeignKey(Conversation, related_name='message_conversation', on_delete=models.CASCADE, null=True)
    message_contents = models.CharField(max_length=300, null=True)
    timestamp = models.DateTimeField(auto_now=True, editable=False)
    image = models.ImageField(upload_to='message_images')
    
    class Meta:
        ordering = ('-id', )