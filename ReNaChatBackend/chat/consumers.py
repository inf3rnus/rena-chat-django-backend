from django.db.models import Q
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message
from .models import Conversation
from users.models import CustomUser
from friends.models import Friend
import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        # Check if the user is authenticated. ID is set by JWT middleware.
        if self.scope['user'].id:
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "chat", self.channel_name)
        self.close(close_code)

    # Used as a controller to detemine which groups should be sent chats

    def receive(self, text_data):
        self.parseCommand(text_data)

    def parseCommand(self, text_data):
        text_data_json = json.loads(text_data)

        command = text_data_json['command']
        print('[parseCommand] - command is: ', command)
        
        if command == 'start_conversation':
            friend_user_id = text_data_json['friend_user_id']
            print('[parseCommand] - friend_user_id is: ', friend_user_id)
            self.startChat(friend_user_id)

        elif command == 'send_chat':
            conversation_id = text_data_json['conversation_id']
            print('[parseCommand] - Target conversation_id is: ', conversation_id)
            print('[parseCommand] - Text_data is: ', text_data)
            self.sendChat(text_data, conversation_id)
            

    def startChat(self, friend_user_id):
        try:
            print('[startChat] - Current user is: ', self.scope['user'].id)
            print('[startChat] - friend_user_id is: ', friend_user_id)
            self.isFriends(self.scope['user'].id, friend_user_id)
            conversation = self.filterConversationByUserlist([self.scope['user'].id, friend_user_id])
            # If both the user and their friend are part of the conversation, add the user to the channels group.
            print('[startChat] - Attempting to add current_user to channel group: ', str(conversation.id))
            async_to_sync(self.channel_layer.group_add)(str(conversation.id), self.channel_name)
            # Return the client with their conversation ID.
            self.send(text_data=json.dumps({
                'client_command': 'start_chat',
                'conversation_id': conversation.id,
            }))
            print('[startChat] - Conversation ID has been sent back to the client!')
        except Exception as e:
            print('[startChat] - ', e)
            self.close()

    def isFriends(self, current_user_id, friend_user_id):
        current_user_friendObj = Friend.objects.get(user_profile=current_user_id)
        current_user_friendObj.friends.get(id=friend_user_id)
        print('[isFriends] - True')


    # There's gotta be a better way to do this...
    def filterConversationByUserlist(self, users):
        query = Q()
        for i in users:
            query &= Q(users=i)
        conversations = Conversation.objects.exclude(~query)
        for i in conversations:
            if i.users.count() == len(users):
                print('[filterConversationByUserlist] - Found conversation_id for users: ', list(users))
                return i
        # If the pair of users does not exist within the db, create a new conversation including them.
        print('[filterConversationByUserlist] - No conversation with users found')
        newConversation = Conversation()
        newConversation.save()
        for i in users:
            newConversation.users.add(i)
            print('[filterConversationByUserlist] - user_id: ', i, ' added to new conversation: ', newConversation.id)
        return newConversation
        

    def sendChat(self, text_data, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            # Verify the user is in the current conversation to prevent cross conversation abuse
            conversation.users.get(id=self.scope['user'].id)

            # Append message ID to broadcasted messages.
            text_data_json = json.loads(text_data)
            message_id = self.saveMessage(text_data_json, conversation)
            text_data_json['message_contents']['_id'] = message_id
            print('[sendChat] - Message ID is: ', message_id)
            text_data = json.dumps(text_data_json)

            async_to_sync(self.channel_layer.group_send)(
                # Group to send to
                str(conversation_id),
                {
                    # Type maps to a class method of ChatConsumer by name
                    "type": "chat.message",
                    "text": text_data,
                },
            )
            print('[sendChat] - Chat successfully sent')

        except Exception as e:
            print('[sendChat] - Error: ', e)
            self.close()

    # TODO Create a message form
    def saveMessage(self, text_data_json, conversation):

        message = Message()
        message.user_profile = self.scope['user']
        message.conversation = conversation
        message.message_contents = json.dumps(text_data_json['message_contents'])
        message.save()
        return message.id

    def chat_message(self, event):
        print('[chat_message] - Event has arrived')
        text_data = event['text']
        typeEvent = event['type']
        print('[chat_message] - Text data is: ', text_data)
        print('[chat_message] - Type of event: ', typeEvent)
        self.send(text_data=text_data)
