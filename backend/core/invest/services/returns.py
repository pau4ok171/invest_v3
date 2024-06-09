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
    market_price_data = [calculate_aggregate_price_data(market) for market in markets]
    sector_market_price_data = [
        calculate_aggregate_price_data(market, sector) for market in markets for sector in sectors
    ]
    company_price_data = [calculate_company_price_data(company) for company in companies]

    update_or_create(market_price_data, sector_market_price_data, company_price_data)


def get_market_list():
    return Market.objects.all()


def get_sector_list():
    return Sector.objects.all()


def calculate_aggregate_price_data(market, sector=None):
    # Получить список компаний по рынку и сектору
    companies = get_company_list(market, sector)

    # Посчитать данные по компании
    companies_market_cap = [calculate_company_market_cap(company) for company in companies]

    market_returns = get_aggregate_returns(companies_market_cap)
    market_returns['market_id'] = market.id
    if sector:
        market_returns['sector_id'] = sector.id
    return market_returns


def calculate_company_price_data(company):
    company_market_cap = calculate_company_market_cap(company)
    price_data = get_aggregate_returns([company_market_cap])
    average_weekly_mouvement = 0
    price_data['company_id'] = company.id
    price_data['average_weekly_mouvement'] = average_weekly_mouvement
    return price_data


def get_company_list(market, sector):
    companies = Company.objects.filter(is_visible=True)

    if market:
        companies = companies.filter(market=market)
    if sector:
        companies = companies.filter(sector=sector)
    return companies


def calculate_company_market_cap(company):
    reports = company.reports
    if not reports.exists():
        return {k: 0 for k in PERIODS.keys()}
    share_outstanding = reports.latest('year', 'quarter').share_outstanding
    prices = get_prices(company)

    return {k: prices[k] * share_outstanding for k in PERIODS.keys()}


def get_aggregate_returns(market_caps):
    cap = {key: sum(map(lambda x: x[key], market_caps)) for key in PERIODS.keys()}
    returns = {f'return_{k}': (cap['now'] - cap[k]) / cap[k] if cap[k] != 0 else 0 for k in cap.keys()}
    returns.pop('return_now')
    return returns


def get_prices(company):
    return {k: get_price(company, PERIODS[k]) for k in PERIODS}


def get_price(company, days):
    time = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=days)
    if company.candles.filter(time__lte=time).exists():
        return company.candles.filter(time__lte=time).latest('time').close
    return 0


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
