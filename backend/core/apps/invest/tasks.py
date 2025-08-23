from celery import shared_task

from apps.invest.services.tinvest import candle_sync
from apps.invest.services.tinvest import dividend_sync
from apps.invest.services.returns import main as returns_main


@shared_task(name='candles', track_started=True)
def candles_task():
    candle_sync()
    return 'candles successful'


@shared_task(name='dividends')
def dividend_task():
    dividend_sync()
    return 'dividends successful'


@shared_task(name='returns')
def returns_task():
    return returns_main()
