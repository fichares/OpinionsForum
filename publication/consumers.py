import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, JsonWebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async
import asyncio

from chat.models import Chat
from person.models import User
from publication.models import Publication


class ChatConsumer(AsyncWebsocketConsumer):
    count_online = 0

    def __int__(self, user):
        self.name = self.requset.user

    async def connect(self):
        ChatConsumer.count_online += 1
        print('connect')
        await self.channel_layer.group_add(
            'General_Chat', self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        ChatConsumer.count_online -= 1

        await self.channel_layer.group_discard(
            'General_Chat', self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):

        text_data = json.loads(text_data)
        print('aaa')
        type = text_data.get("type", None)
        message = text_data.get("text", None)
        author = text_data.get("author", None)

        print(message)

        


    async def online_in_general_chat(self, **kwargs):
        return ChatConsumer.count_online



