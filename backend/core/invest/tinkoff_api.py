import datetime
import logging
from datetime import timedelta
from typing import Optional, List, Dict

import decouple
from asgiref.sync import async_to_sync
from django.db.models import QuerySet
from django.db import transaction
from tinkoff.invest import AsyncClient, CandleInterval, Client
from tinkoff.invest.exceptions import RequestError
from tinkoff.invest.utils import quotation_to_decimal
from channels.layers import get_channel_layer

from invest.models import CandlePerDay, Company

logger = logging.getLogger(__name__)
TOKEN_API = decouple.config('TINKOFF_KEY')


def main() -> List[str]:
    """Основная функция для получения и обработке свечей."""
    try:
        companies = get_visible_companies()
        if not companies.exists():
            logger.warning('No visible companies found')
            return ['No visible companies found']

        results = []
        for company in companies:
            try:
                result = process_company_candles(company)
                results.append(result)

                latest_price = get_latest_price(company)
                if latest_price:
                    send_price_updates(company, latest_price.close)

            except Exception as e:
                logger.error(f'Error processing company {company.id}: {str(e)}')
                results.append(f'Error processing company {company.id}')

        return results

    except Exception as e:
        logger.critical(f'Critical error in main task: {str(e)}')
        return [f'Critical error: {str(e)}']


def get_visible_companies() -> QuerySet:
    """Получить видимые компании."""
    return Company.objects.filter(is_visible=True).only('id', 'uid', 'slug')


def process_company_candles(company: Company) -> str:
    """Обработать свечи для одной компании."""
    candles = get_candles_for_company(company)
    if not candles:
        return f'Company {company.id}: no candles found'

    save_candles(candles)
    return f'Company {company.id}: saved {len(candles)} candles'


def get_candles_for_company(company: Company) -> List[Dict]:
    """Получить свечи для компании из API."""
    date_from = get_start_date(company.id)

    try:
        with Client(TOKEN_API) as client:
            candles = client.get_all_candles(
                instrument_id=company.uid,
                from_=date_from,
                to=datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(days=1),
                interval=CandleInterval.CANDLE_INTERVAL_DAY
            )
            return [prepare_candle_data(company.id, candle) for candle in candles]

    except RequestError as e:
        logger.error(f'API error for company {company.id}: {str(e)}')
        return []
    except Exception as e:
        logger.error(f'Unexpected error for company {company.id}: {str(e)}')
        return []


def get_start_date(company_id: int) -> datetime.datetime:
    """Определить начальную дату для запроса свечей."""
    last_candle = CandlePerDay.objects.filter(
        company_id=company_id,
    ).order_by('-time').first()

    if last_candle:
        return last_candle.time + timedelta(days=1) if last_candle.is_complete else last_candle.time
    return datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)


def prepare_candle_data(company_id: int, candle) -> Dict:
    """Подготовить данные для свечи для сохранения."""
    return {
        'company_id': company_id,
        'open': float(quotation_to_decimal(candle.open)),
        'high': float(quotation_to_decimal(candle.high)),
        'low': float(quotation_to_decimal(candle.low)),
        'close': float(quotation_to_decimal(candle.close)),
        'volume': candle.volume,
        'time': candle.time,
        'is_complete': candle.is_complete,
    }


def save_candles(candles: List[Dict]) -> None:
    """Сохранить свечи в базу данных."""
    with transaction.atomic():
        for candle in candles:
            CandlePerDay.objects.update_or_create(
                company_id=candle['company_id'],
                time=candle['time'],
                defaults=candle,
            )


def get_latest_price(company: Company) -> Optional[CandlePerDay]:
    """Получить последнюю цену компании."""
    try:
        return CandlePerDay.objects.filter(company=company).latest('time')
    except CandlePerDay.DoesNotExist:
        logger.warning(f'No candles found for company {company.id}')
        return None


def send_price_updates(company: Company, price: float) -> None:
    """Отправить обновления цен через каналы."""
    channel_layer = get_channel_layer()
    timestamp = str(datetime.datetime.now())

    async_to_sync(channel_layer.group_send)(
        'price_updates',
        {
            'type': 'send_price_update',
            'data': {
                'uid': company.uid,
                'price': price,
                'timestamp': timestamp
            }
        }
    )

    async_to_sync(channel_layer.group_send)(
        f'company_{company.slug}',
        {
            'type': 'company_price_update',
            'data': {
                'slug': company.slug,
                'price': price,
                'timestamp': timestamp
            }
        }
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print(main())
