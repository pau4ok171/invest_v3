import datetime

import decouple
from tinkoff.invest import GetDividendsResponse, Client, RequestError, Dividend as DividendType
from tinkoff.invest.utils import quotation_to_decimal

from invest.models import Company, Currency, Dividend

TOKEN_API = decouple.config('TINKOFF_KEY')
MILLION_SCALE = 'M'
MILLION_SCALE_UNIT = 1000000


def main():
    companies = get_companies()

    return [process_company_dividends(company) for company in companies]


def get_companies():
    return Company.objects.filter(is_visible=True).values('id', 'uid')


def process_company_dividends(company):
    company_uid = company['uid']
    # Получить список дивидендов по компании из API
    dividends = get_dividends(company_uid)

    if dividends:
        # Обработать полученный массив и собрать список объектов для отправки в БД
        cleaned_dividends = get_cleaned_dividends(dividends, company_uid)

        # Добавить массив объектов к БД
        create_dividend(cleaned_dividends)
        pass


def get_dividends(company_uid: str) -> list[DividendType]:
    try:
        with Client(TOKEN_API) as client:
            dividends_response: GetDividendsResponse = client.instruments.get_dividends(
                instrument_id=company_uid,
                from_=datetime.datetime.utcnow() - datetime.timedelta(days=365 * 30),
                to=datetime.datetime.utcnow() + datetime.timedelta(days=365*30),
            )
        return dividends_response.dividends
    except RequestError as e:
        print(f'[ERROR]: {e}')


def get_cleaned_dividends(dividends: list[DividendType], company_uid: str):
    company = Company.objects.get(uid=company_uid)
    return [{
        'company': company,
        'currency': get_currency(dividend.dividend_net.currency),
        'scale': MILLION_SCALE,
        'scale_unit': MILLION_SCALE_UNIT,
        'dividend_yield': float(quotation_to_decimal(dividend.yield_value)),
        'dividend_amount': get_dividend_amount(dividend.dividend_net, company),
        'declared_date': dividend.declared_date,
        'ex_dividend_date': dividend.last_buy_date,
        'pay_date': dividend.payment_date,
    } for dividend in dividends]


def create_dividend(cleaned_dividends):
    for dividend in cleaned_dividends:
        Dividend.objects.update_or_create(
            company=dividend['company'],
            pay_date=dividend['pay_date'],
            defaults=dividend
        )


def get_currency(currency_iso):
    return Currency.objects.get(name_iso=currency_iso)


def get_dividend_amount(dividend_net, company):
    last_report = None
    share_outstanding = 0
    formatted_dividend_net = float(quotation_to_decimal(dividend_net))

    if company.reports.exists():
        last_report = company.reports.latest('year', 'quarter')

    if last_report:
        share_outstanding = company.reports.latest('year', 'quarter').share_outstanding

    return share_outstanding * formatted_dividend_net / MILLION_SCALE_UNIT
