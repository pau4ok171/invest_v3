from invest.models import Company
from statements import models
from statements.types import Statement


class BaseCheck:
    def __init__(self, fields: dict):
        # Common
        self.statement: Statement | None = None
        self.company_object: Company | None = None
        self.slug: str | None = None
        self.currency: str | None = None
        self.descriptions: dict | None = None
        self.market_country_adjectif: str | None = None
        self.sector_company_name: str | None = None
        # Value
        self.company_current_price: float | None = None
        self.average_price_target_1y: float | None = None
        self.company_fair_price: float | None = None
        self.company_pe: float | None = None
        self.peers_pe: float | None = None
        self.industry_pe: float | None = None
        self.company_fair_pe: float | None = None
        self.return_1y: float | None = None
        self.market_return_1y: float | None = None
        self.sector_market_return_1y: float | None = None
        # Future
        self.company_forecast_earnings_growth: float | None = None
        self.country_saving_rate: float | None = None
        self.market_forecast_earnings_growth: float | None = None
        self.company_forecast_revenue_growth: float | None = None
        self.market_forecast_revenue_growth: float | None = None
        self.company_future_roe_3y: float | None = None
        # Past
        self.company_earnings: float | None = None
        self.company_profit_margins: float | None = None
        self.past_profit_margins: float | None = None
        self.company_earnings_growth_5y: float | None = None
        self.company_earnings_growth: float | None = None
        self.industry_earnings_growth: float | None = None
        self.company_roe: float | None = None
        self.volatility_3m: float | None = None
        self.volatility_1y: float | None = None
        self.volatility_1y_past_year: float | None = None
        self.sector_market_volatility_3m: float | None = None
        # Health
        self.company_short_term_assets: float | None = None
        self.company_short_term_liabilities: float | None = None
        self.company_long_term_liabilities: float | None = None
        self.company_net_debt_to_equity_ratio: float | None = None
        self.company_debt: float | None = None
        self.company_debt_to_equity_ratio: float | None = None
        self.company_debt_to_equity_ratio_5Y_ago: float | None = None
        self.company_operating_cash_flow: float | None = None
        self.company_interest_rate: float | None = None
        self.company_ebit: float | None = None
        # Dividend
        self.company_dividend_yield: float | None = None
        self.market_dividend_yield_p25: float | None = None
        self.market_dividend_yield_p75: float | None = None
        self.company_dividend_is_volatile_in_10y: bool | None = None
        self.company_dividend_amount: float | None = None
        self.company_dividend_amount_10y_ago: float | None = None
        self.company_payout_ratio: float | None = None
        self.company_cash_payout_ratio: float | None = None

        for k, v in fields.items():
            setattr(self, k, v)

        self._process()

    def _process(self):
        self.populate()
        self.check()
        self._create_or_update()
        return f'{self.slug.upper()} on {self.statement["name"]} was {"created" if self.is_created else "updated"}'

    def _create_or_update(self):
        _, self.is_created = models.Statement.objects.update_or_create(
            name=self.statement['name'],
            company=self.statement['company'],
            defaults=self.statement,
        )

    def _validate(self):
        pass

    def check(self):
        pass

    def populate(self):
        pass

    def get_finance_format(self, value):
        return f'{self.currency}{value:.2f}'

    @staticmethod
    def get_multiple_format(value):
        return f'{value:.1f}x'

    @staticmethod
    def get_percent_format(value):
        return f'{value*100:.2f}%'

    def get_finance_format_with_unit(self, value):
        if value == 0:
            return 'n/a'
        for unit in ["", "t", "M", "B", "T"]:
            if abs(value) < 1000:
                return f'{self.currency}{value:.3f}{unit}'
            value /= 1000
        return f'{self.currency}{value:.2f}Q'
