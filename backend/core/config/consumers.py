from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio


class PriceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None

    async def connect(self):
        await self.accept()
        self.room_group_name = "price_updates"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass  # Обработка входящих сообщений от клиента

    async def send_price_update(self, event):
        await self.send(text_data=json.dumps(event['data']))
