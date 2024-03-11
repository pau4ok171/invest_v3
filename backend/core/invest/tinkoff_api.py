import asyncio
import datetime

import decouple
from datetime import timedelta
from dateutil import relativedelta

from invest.models import CandlePerDay, Company
from asgiref.sync import sync_to_async

from tinkoff.invest import AsyncClient, CandleInterval, Client
from tinkoff.invest.utils import now, quotation_to_decimal

TOKEN_API = decouple.config('TINKOFF_KEY')


def main():
    companies = get_companies()

    return [process_company_candles(company) for company in companies]


def get_companies():
    return Company.objects.filter(is_visible=True).values('id', 'uid')


def process_company_candles(company):
    candles = get_candles_by_instrument(instrument_id=company['id'], instrument_uid=company['uid'])
    add_candles_to_db(candles)
    return f'Company({company["id"]}) uid->{company["uid"]} ({len(candles)})candles'


def get_candles_by_instrument(instrument_id, instrument_uid) -> list[dict]:
    date_from = _get_date_from(instrument_id)

    opts = {
        'instrument_id': instrument_uid,
        'from_': date_from,
        'to': datetime.datetime.now(tz=datetime.timezone.utc) + timedelta(days=1),
        'interval': CandleInterval.CANDLE_INTERVAL_DAY
    }

    with Client(TOKEN_API) as client:
        candles = [_get_dict(instrument_id, candle) for candle in client.get_all_candles(**opts)]

    return candles


def add_candles_to_db(candles):
    for candle in candles:
        CandlePerDay.objects.update_or_create(company__pk=candle['company_id'], time=candle['time'], defaults=candle)


def _get_dict(instrument_id, candle):
    return {
        'company_id': instrument_id,
        'open': float(quotation_to_decimal(candle.open)),
        'high': float(quotation_to_decimal(candle.high)),
        'low': float(quotation_to_decimal(candle.low)),
        'close': float(quotation_to_decimal(candle.close)),
        'volume': candle.volume,
        'time': candle.time,
        'is_complete': candle.is_complete,
    }


def _get_date_from(instrument_id) -> datetime.datetime:
    # Получить последнюю свечу из БД и проверить что записи по компании существуют
    candle = CandlePerDay.objects.filter(company__pk=instrument_id).values('time', 'is_complete') or None
    latest = candle.latest('time') if candle else None
    if latest:
        return latest['time'] + timedelta(days=1) if latest['is_complete'] else latest['time']
    else:
        return datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)


def get_info():
    uids = Company.objects.all().values('id', 'uid')
    with Client(TOKEN_API) as client:
        res = [client.instruments.find_instrument(query=uid['uid']) for uid in uids]
        print(res)


def get_candles():
    # Получить список UIDs
    uids = Company.objects.filter(is_visible=True).values('uid')
    with Client(TOKEN_API) as client:
        for uid in uids:
            res = client.instruments.find_instrument(
                query=uid['uid']
            )


if __name__ == '__main__':
    print(main())
