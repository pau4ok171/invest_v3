from typing import Optional, TypeGuard
from dataclasses import asdict
import asyncio
from asgiref.sync import sync_to_async
from tqdm.asyncio import tqdm
import datetime
import json
import logging
import decouple

from django.db import connection
from django.db.models import Exists, OuterRef, Subquery
from django.contrib.auth.models import User
from django.utils import timezone

from tinkoff.invest import (
    AsyncClient,
    Page,
    Instrument as InstrumentDataClass,
    Dividend as DividendDataClass,
    InstrumentResponse,
    CandleInterval,
    HistoricCandle,
)
from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.schemas import PageResponse
from tinkoff.invest.exceptions import AioRequestError
from tinkoff.invest.utils import quotation_to_decimal, money_to_decimal

from apps.invest.models import Company, Instrument, Exchange, Currency, Candle, Dividend
from apps.invest.services.tinvest import InstrumentTask

logger = logging.getLogger(__name__)
TOKEN = decouple.config('TINKOFF_KEY')


class BaseAsyncTinkoffService:
    """Base async service for interaction with Tinkoff Invest API"""

    API_MAX_CALLS = 190 # Api requests
    API_MAX_PERIOD = datetime.timedelta(days=5 * 365) # Days
    API_REQUEST_DELAY = 61 # Seconds

    def __init__(self):
        self._client: Optional[AsyncClient] = None
        self.services: Optional[AsyncServices] = None

    async def __aenter__(self):
        self._client = AsyncClient(TOKEN)
        self.services = await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)
        self.services = None
        self._client = None

    def _check_services(self) -> TypeGuard[AsyncServices]:
        if self.services is None:
            raise RuntimeError('Services not initialized. Use async context manager')
        return True

    async def _process_with_retry(self, func, *args, max_retries=3, **kwargs):
        """Common logic of API retries"""
        for attempt in range(max_retries):
            try:
                return await func(*args, **kwargs)
            except AioRequestError as e:
                if e.code == 429 and attempt < max_retries - 1:
                    await asyncio.sleep(self.API_REQUEST_DELAY * (attempt + 1))
                else:
                    raise
        return None

    async def _process_batch(self, tasks: list, process_func, batch_size: int = None):
        """Processing tasks in batches"""
        batch_size = batch_size or self.API_MAX_CALLS
        progress_bar = tqdm(total=len(tasks))

        while tasks:
            batch = tasks[:batch_size]
            tasks = tasks[batch_size:]

            await asyncio.gather(*(process_func(task) for task in batch))

            if tasks:
                logger.info(f'[Waiting] Waiting {self.API_REQUEST_DELAY}sec before process next batch')
                await asyncio.sleep(self.API_REQUEST_DELAY)

            progress_bar.update(len(batch))

        progress_bar.close()


class TestServiceAsync(BaseAsyncTinkoffService):
    async def get_asset_info(self):
        if not self._check_services():
            return

        result = await self.services.instruments.get_brands_by(id='83904d0e-7864-46bd-9495-a462fcc680a7')
        return result

    async def get_candles(self, instrument_uid):
        if not self._check_services():
            return

        candles = await self.services.market_data.get_candles(
            instrument_id=instrument_uid,
            interval=CandleInterval.CANDLE_INTERVAL_DAY,
            from_=datetime.datetime(year=2014, month=12, day=28, hour=0, minute=0, second=0, microsecond=0),
            to=datetime.datetime(year=2019, month=12, day=26, hour=0, minute=0, second=0, microsecond=0)
        )
        return candles


class BrandServiceAsync(BaseAsyncTinkoffService):
    async def get_brands(self):
        if not self._check_services():
            return

        brands = []
        for i in range(0, 67): # 6592/100=67
            brands_response = await self.services.instruments.get_brands(
                paging=Page(limit=100, page_number=i)
            )
            brands.extend(brands_response.brands)

        brands_dicts = [asdict(brand) for brand in brands]

        with open('brands.json', 'w', encoding='utf-8') as f:
            json.dump(brands_dicts, f, ensure_ascii=False, indent=2)

        print(f'Успешно сохранено {len(brands)} брендов в brands.json')

    async def get_brands_pagination(self) -> Optional[PageResponse]:
        if not self._check_services():
            return

        result = await self.services.instruments.get_brands()
        paging = result.paging

        return paging


class InstrumentServiceAsync(BaseAsyncTinkoffService):
    @staticmethod
    async def get_companies_without_shares() -> list[Company]:
        return await sync_to_async(list)(
            Company.objects.annotate(
                has_share=Exists(
                    Instrument.objects.filter(
                        company_id=OuterRef('pk'),
                        instrument_type='share'
                    )
                )
            ).filter(has_share=False)
        )

    async def get_instrument(
        self,
        ticker: str,
        class_code: str = 'TQBR',
        id_type: int = 2
    ) -> Optional[InstrumentResponse]:
        if not self._check_services():
            return None

        return await self._process_with_retry(
            self.services.instruments.get_instrument_by,
            id=ticker,
            class_code=class_code,
            id_type=id_type,
        )


    @staticmethod
    async def create_or_update_instrument(
        company: Company,
        instrument_data: InstrumentDataClass
    ):
        exchange = await Exchange.objects.aget(mic='XMOS')
        currency = await Currency.objects.aget(iso_code='RUB')
        user = await User.objects.aget(username='admin')

        instrument, _ = await Instrument.objects.aget_or_create(
            ticker=instrument_data.ticker or instrument_data.isin,
            instrument_type=instrument_data.instrument_type,
            defaults={
                'name_ru': instrument_data.name,
                'name_en': '[TBA]',
                'company': company,
                'exchange': exchange,
                'currency': currency,
                'tinkoff_uid': instrument_data.uid,
                'class_code': instrument_data.class_code,
                'isin': instrument_data.isin,
                'lot': instrument_data.lot,
                'created_by': user,
                'updated_by': user,
            }
        )

        return instrument

    async def process_instrument_creation(self, company: Company):
        raise ValueError('We need to reword instrument getting cause company no longer have ticker row')
        instrument_response = await self.get_instrument_response('company.ticker')
        if instrument_response:
            await self.create_or_update_instrument(company, instrument_response.instrument)

    async def create_instruments_for_companies(self, companies: list[Company]):
        await asyncio.gather(*(
            self.process_instrument_creation(company)
            for company in companies)
        )


class CandleServiceAsync(BaseAsyncTinkoffService):
    API_MAX_CALLS = 290 # Per minute (300)

    async def get_candles(self, task: InstrumentTask):
        if not self._check_services():
            return None

        return await self._process_with_retry(
            self.services.market_data.get_candles,
            instrument_id=task.instrument_uid,
            interval=CandleInterval.CANDLE_INTERVAL_DAY,
            from_=task.start_date,
            to=task.end_date,
        )

    async def process_tasks(self, tasks: list[InstrumentTask]):
        semaphore = asyncio.Semaphore(self.API_MAX_CALLS)

        async def process_task(task: InstrumentTask):
            async with semaphore:
                logger.info(f'[Processing] {task.instrument_uid} [{task.start_date} - {task.end_date}]')
                candles = await self.get_candles(task)

                if candles and candles.candles:
                    await self.save_candles(task, candles.candles)
                    logger.info(f'[Saved] {task.instrument_uid} [{task.start_date} - {task.end_date}]')

        await self._process_batch(tasks, process_task)

    async def get_tasks(self, instruments: list[Instrument]) -> list[InstrumentTask]:
        tasks = []
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        last_candles = await self.get_last_candles(instruments)

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
    async def get_last_candles(instruments: list[Instrument]) -> dict[int, Candle]:
        instrument_ids = [i.id for i in instruments]

        if connection.vendor == 'postgresql':
            query = (Candle.objects.filter(instrument_id__in=instrument_ids))
            query = query.order_by('instrument_id', '-time').distinct('instrument_id')
        else:
            subquery = Candle.objects.filter(instrument_id=OuterRef('instrument_id'))
            subquery = subquery.order_by('-time').values('id')[:1]
            query = Candle.objects.filter(id__in=Subquery(subquery))

        return {c.instrument_id: c async for c in query}

    async def save_candles(self, task: InstrumentTask, candles: list[HistoricCandle]):
        instrument = await Instrument.objects.aget(tinkoff_uid=task.instrument_uid)
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

        await Candle.objects.abulk_create(
            candle_objs,
            update_conflicts=True,
            update_fields=['open', 'high', 'low', 'close', 'volume', 'is_complete'],
            unique_fields=['instrument', 'time']
        )


class DividendServiceAsync(BaseAsyncTinkoffService):
    async def get_dividends(self, task: InstrumentTask):
        if not self._check_services():
            return None

        return await self._process_with_retry(
            self.services.instruments.get_dividends,
            instrument_id=task.instrument_uid,
            from_=task.start_date,
            to=task.end_date,
        )

    async def process_tasks(self, tasks: list[InstrumentTask]):
        semaphore = asyncio.Semaphore(self.API_MAX_CALLS)

        async def process_task(task: InstrumentTask):
            async with semaphore:
                dividends = await self.get_dividends(task)
                if dividends and dividends.dividends:
                    await self.save_dividends(task.instrument_uid, dividends.dividends)

        await self._process_batch(tasks, process_task)

    @staticmethod
    async def get_tasks(instruments: list[Instrument]) -> list[InstrumentTask]:
        start_date = datetime.datetime(2000, 8, 21, 0, 0, 0, 0, datetime.timezone.utc)
        end_date = timezone.now() + datetime.timedelta(days=5*365)

        return [
            InstrumentTask(start_date, end_date, i.tinkoff_uid)
            for i in instruments
        ]

    @staticmethod
    async def save_dividends(instrument_uid: str, dividends: list[DividendDataClass]):
        instrument = await Instrument.objects.aget(tinkoff_uid=instrument_uid)
        currency_codes = list(set([d.dividend_net.currency.upper() for d in dividends]))

        currencies = await sync_to_async(dict)(
            Currency.objects.filter(iso_code__in=currency_codes).values_list('iso_code', 'id')
        )

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

        await Dividend.objects.abulk_create(
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

async def dividend_main():
    async with DividendServiceAsync() as service:
        # Get Queryset
        shares = await sync_to_async(list)(Instrument.objects.filter(instrument_type='share'))
        # Get Tasks
        tasks = await service.get_tasks(shares)
        # Process Tasks
        await service.process_tasks(tasks)


async def candle_main():
    async with CandleServiceAsync() as service:
        # Get Queryset
        instruments = await sync_to_async(list)(Instrument.objects.all())
        # Get Tasks
        tasks = await service.get_tasks(instruments)
        # Process Tasks
        await service.process_tasks(tasks)


async def instrument_main():
    async with InstrumentServiceAsync() as service:
        # Get Queryset
        companies = await service.get_companies_without_shares()
        # Process Tasks
        await service.create_instruments_for_companies(companies)


async def test_main():
    async with TestServiceAsync() as service:
        # result = await service.get_asset_info()
        result = await service.get_candles('7de75794-a27f-4d81-a39b-492345813822')
        print(result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    # asyncio.run(instrument_main())
    # asyncio.run(test_main())
    asyncio.run(candle_main())
    # asyncio.run(dividend_main())