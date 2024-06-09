import datetime

from invest.models import Market, Company, Sector, SectorMarket

PERIODS = {
    'now': 0,
    '7d': 7,
    '30d': 30,
    '90d': 90,
    '1y': 365*1,
    '3y': 365*3,
    '5y': 365*5,
}


def main():
    # Получить список
    markets = get_market_list()
    sectors = get_sector_list()
    companies = get_company_list(market=None, sector=None)

    # Посчитать данные
    company_price_data = [get_company_price_data(company) for company in companies]
    sector_market_price_data = [
        get_aggregate_price_data(company_price_data, market=market, sector=sector)
        for market in markets for sector in sectors
    ]
    market_price_data = [get_aggregate_price_data(company_price_data, market=market) for market in markets]

    update_or_create(market_price_data, sector_market_price_data, company_price_data)


def get_company_price_data(company):
    price_data = get_company_returns(company)
    average_weekly_mouvement = get_average_weekly_mouvement(company)
    price_data['company_id'] = company.id
    price_data['company'] = company
    price_data['average_weekly_mouvement'] = average_weekly_mouvement
    return price_data


def get_company_returns(company) -> dict:
    prices = get_prices(company)
    returns = {
        f'return_{k}': (prices['now'].close - prices[k].close) / prices[k].close
        if prices[k] != 0 and prices[k].close != 0 else 0 for k in prices.keys()
    }
    return returns


def get_prices(company):
    return {k: get_price(company, PERIODS[k]) for k in PERIODS}


def get_price(company, days):
    time = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=days)
    if company.candles.filter(time__lte=time).exists():
        return company.candles.filter(time__lte=time).latest('time')
    return 0


def get_aggregate_price_data(companies, market, sector=None):
    companies = list(filter(lambda x: x['company'].market.id == market.id, companies))
    if sector:
        companies = list(filter(lambda x: x['company'].sector.id == sector.id, companies))

    price_data = {
        f'return_{key}': sum(map(lambda x: x[f'return_{key}'], companies)) / len(companies)
        if len(companies) != 0 else 0 for key in PERIODS.keys()
    }
    average_weekly_mouvement = 0
    if companies:
        average_weekly_mouvement = sum(map(lambda x: x['average_weekly_mouvement'], companies)) / len(companies)

    price_data['average_weekly_mouvement'] = average_weekly_mouvement
    price_data['market_id'] = market.id
    if sector:
        price_data['sector_id'] = sector.id

    return price_data


def get_market_list():
    return Market.objects.all()


def get_sector_list():
    return Sector.objects.all()


def get_company_list(market, sector):
    companies = Company.objects.filter(is_visible=True)

    if market:
        companies = companies.filter(market=market)
    if sector:
        companies = companies.filter(sector=sector)
    return companies


def update_or_create(market_price_data, sector_market_price_data, company_price_data):
    [Market.objects.update_or_create(
        pk=price_data['market_id'],
        defaults=price_data
    ) for price_data in market_price_data]

    [SectorMarket.objects.update_or_create(
        market__pk=price_data['market_id'],
        sector__pk=price_data['sector_id'],
        defaults=price_data
    ) for price_data in sector_market_price_data]

    [Company.objects.update_or_create(
        pk=price_data['company_id'],
        defaults=price_data
    ) for price_data in company_price_data]


def get_average_weekly_mouvement(company) -> int:
    time = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=7)
    candles = company.candles.filter(time__gte=time)
    if candles.exists():
        return sum(map(lambda x: (x.high - x.low) / x.high, candles)) / len(candles)
    return 0
