import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ConversationMessage


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f"chat_{self.scope['user'].id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        # Not handling message sending here for detection-only purposes
        pass

    async def new_message(self, event):

        await self.send(
            text_data=json.dumps(
                {
                    "message": "New message received",
                    "sender": event["sender"],
                }
            )
        )

    @staticmethod
    def notify_user(user_id, sender):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync

        print(
            f"Notifying user {user_id} about a new message from {sender.username}"
        )  # Debugging

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{user_id}",
            {
                "type": "new_message",
                "sender": sender.username,
            },
        )
