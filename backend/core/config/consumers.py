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
        self.instrument_uid = None

    async def connect(self):
        self.instrument_uid = self.scope['url_route']['kwargs']['instrument_uid']
        self.group_name = f'instrument_{self.instrument_uid}'

        if await self.is_instrument_accessible():
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

    async def is_instrument_accessible(self):
        # Импорт модели ВНУТРИ метода
        from apps.invest.models import Instrument

        return Instrument.objects.filter(tinkoff_uid=self.instrument_uid).aexists()
