import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User, Chat_message, Messenger_message



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # My functions

    def new_chat_message(self, chat_message, author):
        account = User.objects.get(username=author)
        return Chat_message.objects.create(text=chat_message, author=account)

    def load_chat_messages(self):
        messages = Chat_message.objects.all()[:20]        
        ms_list = []
        for message in messages:
            ms_list.append(message)
        self.messages_to_json(reversed(ms_list))

    def load_messenger_messages(self, room_name):
        messages = Messenger_message.objects.filter(room_name=room_name)
        ms_list = []
        for message in messages:
            ms_list.append(message)
        self.messages_to_json(reversed(ms_list))

    def messages_to_json(self, ms_list):
        for message in ms_list:
            self.send_ms(message)

    def send_ms(self, message):
        self.send(text_data=json.dumps({
            'message': message.text,
            'author': message.author.username,
            'timestamp': str(message.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        }, ensure_ascii=False))      

    def new_messenger_message(self, messenger_message, author, companion, room_name):
        account = User.objects.get(username=author)
        companion = User.objects.get(username=companion)
        return Messenger_message.objects.create(author=account,
                                                companion=companion,
                                                text=messenger_message,
                                                room_name=room_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        json_data = json.loads(text_data)
        if json_data['command'] == 'new_chat_message':
            chat_message = json_data['message']
            if chat_message == '':
                return
            else:    
                author = json_data['account']
                new_chat_message = self.new_chat_message(chat_message, author)
                self.group_send(new_chat_message)
       
        elif json_data['command'] == 'load_chat_messages':
            self.load_chat_messages()

        elif json_data['command'] == 'new_messenger_message':
            messenger_message = json_data['message']
            if messenger_message == '':
                return
            else:    
                author = json_data['account']
                companion = json_data['companion']
                room_name = json_data['room_name']
                new_messenger_message = self.new_messenger_message(messenger_message, author, companion, room_name)
                self.group_send(new_messenger_message)



        elif json_data['command'] == 'load_messenger_messages':
            room_name = json_data['room_name']
            self.load_messenger_messages(room_name)

       
       
        # Send message to room group
    def group_send(self, message):    
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.text,
                'timestamp': str(message.timestamp.strftime("%Y-%m-%d %H:%M:%S")),
                'author': message.author.username
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        timestamp = event['timestamp']
        author = event['author']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'timestamp': timestamp,
            'author': author
        }))