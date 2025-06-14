import calendar
import datetime

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
        # Risks
        self.earnings_growth_per_year_forecast_3y: float | None = None
        self.capitalisation_rate: float | None = None
        self.capitalisation_rate_1y: float | None = None
        self.operating_cash_flow_growth: float | None = None
        self.gross_profit_margin: float | None = None
        self.gross_profit_margin_1y: float | None = None
        self.sloan_ratio: float | None = None
        self.inventory_growth: float | None = None
        self.sales_growth: float | None = None
        self.unearned_revenue_growth: float | None = None
        self.accounts_receivable_growth: float | None = None
        self.one_off_charges: float | None = None
        self.market_cap: float | None = None
        self.market_cap_usd: float | None = None
        self.revenue: float | None = None
        self.events_was_occurred: bool | None = None
        self.substantial_insider_selling_was_occurred: bool | None = None
        self.has_diluted_over_past_year: bool | None = None
        self.non_operating_revenue: float | None = None
        self.operating_revenue: float | None = None
        self.cash_and_cash_equivalents: float | None = None
        self.cash_expenses: float | None = None
        self.equity: float | None = None

        for k, v in fields.items():
            setattr(self, k, v)

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'statement': self.statement,
            'result': self._process()
        }

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

    def get_report_diff(self) -> datetime.timedelta | None:
        reports = self.company_object.reports
        if reports.exists():
            report = reports.latest('year', 'quarter')
            month = 12 if report.quarter == 0 else report.quarter * 3
            _, last_day = calendar.monthrange(report.year, month)
            report_date = datetime.datetime(report.year, month, last_day)
            return datetime.datetime.now() - report_date
