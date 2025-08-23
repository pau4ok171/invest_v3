from time import sleep
from typing import Optional, TypeGuard
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from tqdm import tqdm as sync_tqdm
import datetime
import logging
import decouple

from django.db import connection
from django.db.models import OuterRef, Subquery, QuerySet
from django.utils import timezone

from tinkoff.invest import (
    Client,
    Dividend as DividendDataClass,
    CandleInterval,
    HistoricCandle,
)
from tinkoff.invest.services import Services
from tinkoff.invest.exceptions import AioRequestError
from tinkoff.invest.utils import quotation_to_decimal, money_to_decimal

from apps.invest.models import Instrument, Currency, Candle, Dividend

logger = logging.getLogger(__name__)
TOKEN = decouple.config('TINKOFF_KEY')

class InstrumentTask:
    start_date = None
    end_date = None
    instrument_uid = None

    def __init__(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        instrument_uid: str
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.instrument_uid = instrument_uid

    def __repr__(self):
        return f'InstrumentTask({self.instrument_uid} [{self.start_date}] - [{self.end_date}])'


class BaseTinkoffService:
    """Base service for interaction with Tinkoff Invest API"""
    API_MAX_CALLS = 190 # Api requests
    API_MAX_PERIOD = datetime.timedelta(days=5 * 365) # Days
    API_REQUEST_DELAY = 61 # Seconds

    def __init__(self):
        self._client: Optional[Client] = None
        self.services: Optional[Services] = None

    def __enter__(self):
        self._client = Client(TOKEN)
        self.services = self._client.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            self._client.__exit__(exc_type, exc_val, exc_tb)
        self.services = None
        self._client = None

    def _check_services(self) -> TypeGuard[Services]:
        if self.services is None:
            raise RuntimeError('Services not initialized. Use context manager')
        return True

    def _process_with_retry(self, func, *args, max_retries=3, **kwargs):
        """Common logic of API retries"""
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except AioRequestError as e:
                if e.code == 429 and attempt < max_retries - 1:
                    sleep(self.API_REQUEST_DELAY * (attempt + 1))
                else:
                    raise
        return None

    def _process_batch(self, tasks: list, process_func, batch_size: int = None):
        """Processing tasks in batches"""
        batch_size = batch_size or self.API_MAX_CALLS
        progress_bar = sync_tqdm(total=len(tasks))

        while tasks:
            batch = tasks[:batch_size]
            tasks = tasks[batch_size:]

            for task in batch:
                process_func(task)

            if tasks:
                logger.info(f'[Waiting] Waiting {self.API_REQUEST_DELAY}sec before process next batch')
                sleep(self.API_REQUEST_DELAY)

            progress_bar.update(len(batch))

        progress_bar.close()


class CandleService(BaseTinkoffService):
    API_MAX_CALLS = 290 # Per minute (300)

    def get_candles(self, task: InstrumentTask):
        if not self._check_services():
            return None

        return self._process_with_retry(
            self.services.market_data.get_candles,
            instrument_id=task.instrument_uid,
            interval=CandleInterval.CANDLE_INTERVAL_DAY,
            from_=task.start_date,
            to=task.end_date,
        )

    def process_tasks(self, tasks: list[InstrumentTask]):
        def process_task(task: InstrumentTask):
            logger.info(f'[Processing] {task.instrument_uid} [{task.start_date} - {task.end_date}]')
            candles = self.get_candles(task)

            if candles and candles.candles:
                self.save_candles(task, candles.candles)
                logger.info(f'[Saved] {task.instrument_uid} [{task.start_date} - {task.end_date}]')

        self._process_batch(tasks, process_task)

    def get_tasks(self, instruments: QuerySet[Instrument]) -> list[InstrumentTask]:
        tasks = []
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_candles = self.get_last_candles(instruments)

        for instrument in instruments:
            start_date = self.get_start_date(last_candles.get(instrument.id))
            tasks.extend(self.create_tasks_for_period(instrument.tinkoff_uid, start_date, today))

        return tasks

    @staticmethod
    def get_start_date(
        last_candle: Optional[Candle]
    ) -> datetime.datetime:
        if last_candle:
            return last_candle.time + datetime.timedelta(days=1) if last_candle.is_complete else last_candle.time

        return datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)

    def create_tasks_for_period(
        self,
        instrument_uid: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime
    ) -> list[InstrumentTask]:
        tasks = []
        current_start = start_date

        while current_start <= end_date:
            current_end = min(
                current_start + self.API_MAX_PERIOD,
                end_date
            )

            tasks.append(InstrumentTask(
                start_date=current_start,
                end_date=current_end,
                instrument_uid=instrument_uid
            ))

            current_start = current_end + datetime.timedelta(days=1)

        return tasks

    @staticmethod
    def get_last_candles(instruments: QuerySet[Instrument]) -> dict[int, Candle]:
        instrument_ids = [i.id for i in instruments]

        if connection.vendor == 'postgresql':
            query = (Candle.objects.filter(instrument_id__in=instrument_ids))
            query = query.order_by('instrument_id', '-time').distinct('instrument_id')
        else:
            subquery = Candle.objects.filter(instrument_id=OuterRef('instrument_id'))
            subquery = subquery.order_by('-time').values('id')[:1]
            query = Candle.objects.filter(id__in=Subquery(subquery))

        return {c.instrument_id: c for c in query}

    def save_candles(self, task: InstrumentTask, candles: list[HistoricCandle]):
        instrument = Instrument.objects.get(tinkoff_uid=task.instrument_uid)
        candle_objs = []
        latest_prices = {} # {instrument_uid: price}

        for candle in candles:
            close = float(quotation_to_decimal(candle.close))
            candle_objs.append(Candle(
                instrument=instrument,
                time=candle.time,
                open=float(quotation_to_decimal(candle.open)),
                high=float(quotation_to_decimal(candle.high)),
                low=float(quotation_to_decimal(candle.low)),
                close=close,
                volume=candle.volume,
                is_complete=candle.is_complete
            ))
            latest_prices[instrument.tinkoff_uid] = close

        Candle.objects.bulk_create(
            candle_objs,
            update_conflicts=True,
            update_fields=['open', 'high', 'low', 'close', 'volume', 'is_complete'],
            unique_fields=['instrument', 'time']
        )

        self.send_bulk_price_updates(latest_prices)

    @staticmethod
    def send_bulk_price_updates(price_updates: dict[str, float]) -> None:
        """Отправить обновления цен через каналы."""
        channel_layer = get_channel_layer()
        timestamp = str(datetime.datetime.now(datetime.timezone.utc))

        for uid, price in price_updates.items():
            # For Company List
            async_to_sync(channel_layer.group_send)(
                'price_updates',
                {
                    'type': 'send_price_update',
                    'data': {
                        'uid': uid,
                        'price': price,
                        'timestamp': timestamp
                    }
                }
            )

            # For Company Detail
            async_to_sync(channel_layer.group_send)(
                f'instrument_{uid}',
                {
                    'type': 'instrument_price_update',
                    'data': {
                        'uid': uid,
                        'price': price,
                        'timestamp': timestamp
                    }
                }
            )


class DividendService(BaseTinkoffService):
    def get_dividends(self, task: InstrumentTask):
        if not self._check_services():
            return None

        return self._process_with_retry(
            self.services.instruments.get_dividends,
            instrument_id=task.instrument_uid,
            from_=task.start_date,
            to=task.end_date,
        )

    def process_tasks(self, tasks: list[InstrumentTask]):
        def process_task(task: InstrumentTask):
            dividends = self.get_dividends(task)
            if dividends and dividends.dividends:
                self.save_dividends(task.instrument_uid, dividends.dividends)

        self._process_batch(tasks, process_task)

    @staticmethod
    def get_tasks(instruments: QuerySet[Instrument]) -> list[InstrumentTask]:
        start_date = datetime.datetime(2000, 8, 21, 0, 0, 0, 0, datetime.timezone.utc)
        end_date = timezone.now() + datetime.timedelta(days=5*365)

        return [
            InstrumentTask(start_date, end_date, i.tinkoff_uid)
            for i in instruments
        ]

    @staticmethod
    def save_dividends(instrument_uid: str, dividends: list[DividendDataClass]):
        instrument = Instrument.objects.get(tinkoff_uid=instrument_uid)
        currency_codes = list(set([d.dividend_net.currency.upper() for d in dividends]))

        currencies = dict(Currency.objects.filter(iso_code__in=currency_codes).values_list('iso_code', 'id'))

        dividends_objs = []
        for d in dividends:
            currency_id = currencies.get(d.dividend_net.currency.upper())

            if not currency_id:
                logger.critical(f'for task {instrument_uid} there is not appropriate currency')
                continue

            dividends_objs.append(Dividend(
                instrument=instrument,
                currency_id=currency_id,
                dividend_net=float(money_to_decimal(d.dividend_net)),
                payment_date=d.payment_date,
                declared_date=d.declared_date,
                ex_dividend_date=d.last_buy_date,
                dividend_type=d.dividend_type,
                record_date=d.record_date,
                regularity=d.regularity,
                close_price=float(money_to_decimal(d.close_price)),
                yield_value=float(quotation_to_decimal(d.yield_value)),
            ))

        Dividend.objects.bulk_create(
            dividends_objs,
            update_conflicts=True,
            update_fields=[
                'currency',
                'dividend_net',
                'payment_date',
                'declared_date',
                'ex_dividend_date',
                'dividend_type',
                'record_date',
                'regularity',
                'close_price',
                'yield_value',
            ],
            unique_fields=['instrument', 'record_date']
        )


def dividend_sync():
    with DividendService() as service:
        shares = Instrument.objects.filter(instrument_type='share')
        tasks = service.get_tasks(shares)
        service.process_tasks(tasks)


def candle_sync():
    with CandleService() as service:
        instruments = Instrument.objects.all()
        tasks = service.get_tasks(instruments)
        service.process_tasks(tasks)
