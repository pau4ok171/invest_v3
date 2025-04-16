from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import json


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


class CompanyDetailPriceConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None
        self.company_slug = None

    async def connect(self):
        self.company_slug = self.scope['url_route']['kwargs']['company_slug']
        self.group_name = f'company_{self.company_slug}'

        if await self.is_company_accessible():
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass  # Обработка входящих сообщений от клиента

    async def company_price_update(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def is_company_accessible(self):
        # Импорт модели ВНУТРИ метода
        from invest.models import Company

        return Company.objects.filter(slug=self.company_slug).exists()
