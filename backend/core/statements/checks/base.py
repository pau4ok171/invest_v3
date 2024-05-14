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
        self.company_sector_name: str | None = None
        # Value
        self.current_price: float | None = None
        self.fair_price: float | None = None
        self.company_pe: float | None = None
        self.peers_pe: float | None = None
        self.industry_pe: float | None = None
        self.fair_pe: float | None = None
        # Future
        self.forecast_earnings_growth: float | None = None
        self.saving_rate: float | None = None
        self.market_forecast_earnings_growth: float | None = None
        self.forecast_revenue_growth: float | None = None
        self.market_forecast_revenue_growth: float | None = None
        self.future_roe_3y: float | None = None
        # Past
        self.net_income: float | None = None
        self.profit_margins: float | None = None
        self.past_profit_margins: float | None = None
        self.net_income_growth_5y: float | None = None
        self.earnings_growth: float | None = None
        self.industry_earnings_growth: float | None = None
        self.company_roe: float | None = None
        # Health
        self.short_term_assets: float | None = None
        self.short_term_liabilities: float | None = None
        self.long_term_liabilities: float | None = None
        self.debt_to_equity_ratio: float | None = None
        self.debt: float | None = None
        self.debt_5Y_ago: float | None = None
        self.operating_cash_flow: float | None = None
        self.interest_rate: float | None = None
        self.company_ebit: float | None = None
        # Dividend
        self.dividend_yield: float | None = None
        self.market_dividend_yield_p25: float | None = None
        self.market_dividend_yield_p75: float | None = None
        self.dividend_is_volatile_in_10y: bool | None = None
        self.dividend_amount: float | None = None
        self.dividend_amount_10y_ago: float | None = None
        self.payout_ratio: float | None = None
        self.cash_payout_ratio: float | None = None

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
