from celery import shared_task
import asyncio
from invest.tinkoff_api import main
from invest.services.dividend import main as dividend_main
from invest.services.returns import main as returns_main


@shared_task(name='Tinkoff_API')
def tinkoff_task():
    return main()


@shared_task(name='dividends')
def dividend_task():
    return dividend_main()


@shared_task(name='returns')
def returns_task():
    return returns_main()
