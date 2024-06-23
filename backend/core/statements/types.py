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
    outcome: int


class Fields(TypedDict):
    # Common
    company_object: Company
    slug: str
    currency: str
    market_country_adjectif: str
    sector_company_name: str
    # Value
    company_current_price: float
    average_price_target_1y: float
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
    return_1y: float
    market_return_1y: float
    sector_market_return_1y: float
    # Past
    company_earnings: float
    company_profit_margins: float
    past_profit_margins: float
    company_earnings_growth_5y: float
    company_earnings_growth: float
    industry_earnings_growth: float
    company_roe: float
    volatility_3m: float
    volatility_1y: float
    volatility_1y_past_year: float
    sector_market_volatility_3m: float
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
    # Risks
    earnings_growth_per_year_forecast_3y: float
    capitalisation_rate: float
    capitalisation_rate_1y: float
    operating_cash_flow_growth: float
    gross_profit_margin: float
    gross_profit_margin_1y: float
    sloan_ratio: float
    inventory_growth: float
    sales_growth: float
    unearned_revenue_growth: float
    accounts_receivable_growth: float
    one_off_charges: float
    market_cap: float
    market_cap_usd: float
    revenue: float
    events_was_occurred: bool
    substantial_insider_selling_was_occurred: bool
    has_diluted_over_past_year: bool
    non_operating_revenue: float
    operating_revenue: float
    cash_and_cash_equivalents: float
    cash_expenses: float
    equity: float
