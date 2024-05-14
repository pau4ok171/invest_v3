from enum import Enum
from typing import TypedDict
from invest.models import Company


class ExtendedEnum(Enum):
    @classmethod
    def as_dict(cls):
        return dict(map(lambda item: (item.name, item.value.capitalize()), cls))

    def __str__(self):
        return self.name


class Level(ExtendedEnum):
    INIT = 'INIT'
    GLOBAL = 'GLOBAL'
    SECTOR = 'SECTOR'


class Area(ExtendedEnum):
    RISKS = 'RISKS'
    REWARDS = 'REWARDS'
    OVERVIEW = 'OVERVIEW'
    VALUE = 'VALUE'
    FUTURE = 'FUTURE'
    PAST = 'PAST'
    HEALTH = 'HEALTH'
    DIVIDENDS = 'DIVIDENDS'
    MANAGEMENT = 'MANAGEMENT'
    OWNERSHIP = 'OWNERSHIP'
    MISC = 'MISC'


class Type(ExtendedEnum):
    RISKS = 'RISKS'
    STATEMENTS = 'STATEMENTS'
    REWARDS = 'REWARDS'


class Status(ExtendedEnum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    NODATA = 'NODATA'


class Severity(ExtendedEnum):
    NONE = 'NONE'
    MINOR = 'MINOR'
    MAJOR = 'MAJOR'


class Statement(TypedDict):
    company: Company
    name: str
    title: str
    description: str
    question: str
    level: Level
    area: Area
    type: Type
    status: Status
    severity: Severity


class Fields(TypedDict):
    # Common
    company_object: Company
    slug: str
    currency: str
    market_country_adjectif: str
    sector_company_name: str
    # Value
    company_current_price: float
    company_fair_price: float
    company_pe: float
    peers_pe: float
    industry_pe: float
    company_fair_pe: float
    # Future
    company_forecast_earnings_growth: float
    country_saving_rate: float
    market_forecast_earnings_growth: float
    company_forecast_revenue_growth: float
    market_forecast_revenue_growth: float
    company_future_roe_3y: float
    # Past
    company_earnings: float
    company_profit_margins: float
    past_profit_margins: float
    company_earnings_growth_5y: float
    company_earnings_growth: float
    industry_earnings_growth: float
    company_roe: float
    # Health
    company_short_term_assets: float
    company_short_term_liabilities: float
    company_long_term_liabilities: float
    company_net_debt_to_equity_ratio: float
    company_debt: float
    company_debt_to_equity_ratio: float
    company_debt_to_equity_ratio_5Y_ago: float
    company_operating_cash_flow: float
    company_interest_rate: float
    company_ebit: float
    # Dividend
    company_dividend_yield: float
    market_dividend_yield_p25: float
    market_dividend_yield_p75: float
    company_dividend_is_volatile_in_10y: bool
    company_dividend_amount: float
    company_dividend_amount_10y_ago: float
    company_payout_ratio: float
    company_cash_payout_ratio: float
