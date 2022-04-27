import json
from django.contrib.auth import get_user_model
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Message
User = get_user_model()
class ChatConsumer(WebsocketConsumer):
    # send message based on command
    def fetch_messages(self,data):
        messages = Message.show_10_msg()
        content = {
            'messages':self.messages_to_json(messages)
        }
        self.send_message(content)
        
    def new_messages(self,data):
        author = data['from']
        author_user = User.filter(username=author)[0]
        message = Message.objects.create(author=author_user,content=data['message'])
        content={
            'command':'new_messages',
            'message':self.message_to_json(message)
        }
        return self.send_chat_msg(content)
    
    def messages_to_json(self,messages):
        #serialize messages
        result = []
        for msg in messages:
            result.append(self.message_to_json(msg))
        return result
    
    def message_to_json(self,msg):
        return {
            'author':msg.author.username,
            'content':msg.content,
            'timestamp':str(msg.timestamp),
        }
        
    
    
    commands = {
        'fetch_messages':fetch_messages,
        'new_messages':new_messages
    }
    
    def connect(self):
        """add user to the group."""
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self,close_code):
        # Leave room group
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )
        
    # Receive message from Websocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_msg(self,message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )
        
    def send_message(self, message):
        self.send(text_data=json.dumps(message))
        
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to Websocket
        self.send(text_data=json.dumps(message))