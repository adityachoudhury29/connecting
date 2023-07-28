import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from lprofile.models import profile1
from django.core.files.base import ContentFile
import os

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]
        try:
            profile = await database_sync_to_async(profile1.objects.get)(profowner=user)
            imgurl = profile.profimg.url if profile.profimg else ""
        except profile1.DoesNotExist:
            imgurl = ""

        room1 = await database_sync_to_async(room.objects.get)(name=self.room_name)

        if "file_data" in text_data_json:
            file_data = text_data_json["file_data"]
            file_name = text_data_json["file_name"]
            file_content = ContentFile(file_data, name=file_name)
            chat = messages(content=file_name, sender=user, roomname=room1, file=file_content)
            await database_sync_to_async(chat.save)()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": file_name,
                    "username": user.username,
                    "imgurl": imgurl,
                    "timestamp": chat.timestamp.strftime("%B %d, %Y, %H:%M"),
                    "file_url": chat.file.url,
                },
            )

        else:
            chat=messages(content=message,sender=self.scope['user'],roomname=room1)
            await database_sync_to_async(chat.save)()
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat.message", "message": message, "username":user.username, "imgurl":imgurl, "timestamp":chat.timestamp.strftime("%B %d, %Y, %H:%M")}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        imgurl = event["imgurl"]
        timestamp = event["timestamp"]
        file_url = event.get("file_url", None)

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "imgurl": imgurl,
                    "timestamp": timestamp,
                    "file_url": file_url,
                }
            )
        )
