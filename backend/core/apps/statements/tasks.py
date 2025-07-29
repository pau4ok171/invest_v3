from celery import shared_task
from apps.statements.services.analysis import main


@shared_task(name='StatementCheck')
def statement_check_task():
    return main()
