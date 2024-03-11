from celery import shared_task
import asyncio
from invest.tinkoff_api import main


@shared_task(name='Tinkoff_API')
def tinkoff_task():
    return main()
