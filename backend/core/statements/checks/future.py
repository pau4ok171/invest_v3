from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class EarningsVsSavingRateCheck(BaseCheck):
    def check(self) -> None:
        if self.forecast_earnings_growth > self.saving_rate:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsExpectedProfitGrowthAboveRiskFreeRate',
            title='Earnings vs Savings Rate',
            description='',
            question=f'Is {self.slug.upper()} expected to grow profits faster than the low risk savings rate?',
            level=level.GLOBAL,
            area=area.FUTURE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s '
                       f'forecast earnings growth ({self.forecast_earnings_growth * 100}% per year)'
                       f' is above the savings rate ({self.saving_rate * 100}%).',
            'error': f'{self.slug.upper()}\'s '
                     f'forecast earnings growth ({self.forecast_earnings_growth * 100}% per year)'
                     f' is below the savings rate ({self.saving_rate * 100}%).',
        }


class EarningsVsMarketCheck(BaseCheck):
    def check(self) -> None:
        if self.forecast_earnings_growth > self.market_forecast_earnings_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsExpectedAnnualProfitGrowthAboveMarket',
            title='Earnings vs Market',
            description='',
            question=f'Is {self.slug.upper()} expected to grow profits faster than the market?',
            level=level.GLOBAL,
            area=area.FUTURE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s earnings ({self.forecast_earnings_growth * 100}% per year) '
                       f'are forecast to grow faster than '
                       f'the {self.market_country_adjectif.capitalize()} market '
                       f'({self.market_forecast_earnings_growth * 100}% per year).',
            'error': f'{self.slug.upper()}\'s earnings ({self.forecast_earnings_growth * 100}% per year) '
                     f'are forecast to grow slower than '
                     f'the {self.market_country_adjectif.capitalize()} market '
                     f'({self.market_forecast_earnings_growth * 100}% per year).',
        }


class HighGrowthEarningsCheck(BaseCheck):
    def check(self) -> None:
        if self.forecast_earnings_growth > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsExpectedAnnualProfitGrowthHigh',
            title='High Growth Earnings',
            description='',
            question=f'Is {self.slug.upper()} expected to have high profit growth?',
            level=level.GLOBAL,
            area=area.FUTURE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s earnings are expected to grow significantly over the next 3 years.',
            'error': f'{self.slug.upper()}\'s earnings are forecast to grow, but not significantly.',
        }


class RevenueVsMarketCheck(BaseCheck):
    def check(self) -> None:
        if self.forecast_revenue_growth > self.market_forecast_revenue_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsExpectedRevenueGrowthAboveMarket',
            title='Revenue vs Market',
            description='',
            question=f'Is {self.slug.upper()} revenue growth expected to exceed the market?',
            level=level.GLOBAL,
            area=area.FUTURE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s revenue '
                       f'({self.forecast_revenue_growth * 100}% per year) '
                       f'is forecast to grow faster than the '
                       f'{self.market_country_adjectif} market '
                       f'({self.market_forecast_revenue_growth * 100}% per year).',
            'error': f'{self.slug.upper()}\'s revenue '
                     f'({self.forecast_revenue_growth * 100}% per year) '
                     f'is forecast to grow slower than the '
                     f'{self.market_country_adjectif.capitalize()} market '
                     f'({self.market_forecast_revenue_growth * 100}% per year).',
        }


class HighGrowthRevenueCheck(BaseCheck):
    def check(self) -> None:
        if self.forecast_revenue_growth > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsExpectedRevenueGrowthHigh',
            title='High Growth Revenue',
            description='',
            question=f'Is {self.slug.upper()} expected to have high revenue growth?',
            level=level.GLOBAL,
            area=area.FUTURE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s revenue '
                       f'({self.forecast_revenue_growth * 100}% per year) '
                       f'is forecast to grow faster than 20% per year.',
            'error': f'{self.slug.upper()}\'s revenue '
                     f'({self.forecast_revenue_growth * 100}% per year) '
                     f'is forecast to grow slower than 20% per year.',
        }


class FutureROECheck(BaseCheck):
    def check(self) -> None:
        if self.future_roe_3y > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsReturnOnEquityForecastAboveBenchmark',
            title='Future ROE',
            description='',
            question=f'Is {self.slug.upper()}\'s return on equity forecast to be above 20%?',
            level=level.GLOBAL,
            area=area.FUTURE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s Return on Equity '
                       f'is forecast to be very high in 3 years time ({self.future_roe_3y*100}%).',
            'error': f'{self.slug.upper()}\'s Return on Equity '
                     f'is forecast to be low in 3 years time ({self.future_roe_3y*100}%).',
        }
