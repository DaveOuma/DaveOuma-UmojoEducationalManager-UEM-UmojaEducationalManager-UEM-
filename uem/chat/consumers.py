import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    ChatConsumer handles WebSocket connections for a chat room.

    It manages user connections, message sending and receiving, and 
    broadcasting messages to all users in the chat room.

    Methods:
        connect(): Handles the connection event for the user.
        disconnect(close_code): Handles the disconnection event for the user.
        receive(text_data): Receives messages from WebSocket and broadcasts them.
        chat_message(event): Receives messages from the room group and sends them to WebSocket.
    """

    async def connect(self):
        """
        Handles the user connection to the chat room.

        This method adds the user to the room group and accepts the WebSocket connection.
        """
        self.user = self.scope['user']  # Get the connected user
        self.id = self.scope['url_route']['kwargs']['course_id']  # Get the course ID from the URL
        self.room_group_name = f'chat_{self.id}'  # Create a unique room group name

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the disconnection of the user from the chat room.

        This method removes the user from the room group upon disconnection.
        
        Args:
            close_code (int): The code indicating why the connection was closed.
        """
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receives messages from the WebSocket.

        This method processes incoming messages, formats them, and sends them 
        to the room group for broadcasting.

        Args:
            text_data (str): The text data received from the WebSocket.
        """
        text_data_json = json.loads(text_data)  # Parse JSON message
        message = text_data_json['message']  # Extract the message
        now = timezone.now()  # Get the current time
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,  # Get the username of the sender
                'datetime': now.isoformat(),  # Format the current time in ISO format
            }
        )

    async def chat_message(self, event):
        """
        Receives messages from the room group and sends them to the WebSocket.

        Args:
            event (dict): The event containing the message data to be sent.
        """
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
