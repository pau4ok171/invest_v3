from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class EarningsVsSavingRateCheck(BaseCheck):
    def check(self) -> None:
        if self.company_forecast_earnings_growth > self.country_saving_rate:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_forecast_earnings_growth = self.get_percent_format(self.company_forecast_earnings_growth)
        formatted_saving_rate = self.get_percent_format(self.country_saving_rate)

        self.descriptions = {
            'success': f'{formatted_slug}\'s '
                       f'forecast earnings growth ({formatted_forecast_earnings_growth} per year)'
                       f' is above the savings rate ({formatted_saving_rate}).',
            'error': f'{formatted_slug}\'s '
                     f'forecast earnings growth ({formatted_forecast_earnings_growth} per year)'
                     f' is below the savings rate ({formatted_saving_rate}).',
        }


class EarningsVsMarketCheck(BaseCheck):
    def check(self) -> None:
        if self.company_forecast_earnings_growth > self.market_forecast_earnings_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_country_adjectif = self.market_country_adjectif.capitalize()
        formatted_forecast_earnings_growth = self.get_percent_format(self.company_forecast_earnings_growth)
        formatted_market_forecast_earnings_growth = self.get_percent_format(self.market_forecast_earnings_growth)

        self.descriptions = {
            'success': f'{formatted_slug}\'s earnings ({formatted_forecast_earnings_growth} per year) '
                       f'are forecast to grow faster than '
                       f'the {formatted_country_adjectif} market '
                       f'({formatted_market_forecast_earnings_growth} per year).',
            'error': f'{formatted_slug}\'s earnings ({formatted_forecast_earnings_growth} per year) '
                     f'are forecast to grow slower than '
                     f'the {formatted_country_adjectif} market '
                     f'({formatted_market_forecast_earnings_growth} per year).',
        }


class HighGrowthEarningsCheck(BaseCheck):
    def check(self) -> None:
        if self.company_forecast_earnings_growth > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        self.descriptions = {
            'success': f'{self.slug.upper()}\'s earnings are expected to grow significantly over the next 3 years.',
            'error': f'{self.slug.upper()}\'s earnings are forecast to grow, but not significantly.',
        }


class RevenueVsMarketCheck(BaseCheck):
    def check(self) -> None:
        if self.company_forecast_revenue_growth > self.market_forecast_revenue_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_country_adjectif = self.market_country_adjectif.capitalize()
        formatted_forecast_revenue_growth = self.get_percent_format(self.company_forecast_revenue_growth)
        formatted_market_forecast_revenue_growth = self.get_percent_format(self.market_forecast_revenue_growth)

        self.descriptions = {
            'success': f'{formatted_slug}\'s revenue '
                       f'({formatted_forecast_revenue_growth} per year) '
                       f'is forecast to grow faster than the '
                       f'{formatted_country_adjectif} market '
                       f'({formatted_market_forecast_revenue_growth} per year).',
            'error': f'{formatted_slug}\'s revenue '
                     f'({formatted_forecast_revenue_growth} per year) '
                     f'is forecast to grow slower than the '
                     f'{formatted_country_adjectif} market '
                     f'({formatted_market_forecast_revenue_growth} per year).',
        }


class HighGrowthRevenueCheck(BaseCheck):
    def check(self) -> None:
        if self.company_forecast_revenue_growth > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_forecast_revenue_growth = self.get_percent_format(self.company_forecast_revenue_growth)

        self.descriptions = {
            'success': f'{formatted_slug}\'s revenue '
                       f'({formatted_forecast_revenue_growth} per year) '
                       f'is forecast to grow faster than 20% per year.',
            'error': f'{formatted_slug}\'s revenue '
                     f'({formatted_forecast_revenue_growth} per year) '
                     f'is forecast to grow slower than 20% per year.',
        }


class FutureROECheck(BaseCheck):
    def check(self) -> None:
        if self.company_future_roe_3y > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_future_roe_3y = self.get_percent_format(self.company_future_roe_3y)

        self.descriptions = {
            'success': f'{formatted_slug}\'s Return on Equity '
                       f'is forecast to be very high in 3 years time ({formatted_future_roe_3y}).',
            'error': f'{formatted_slug}\'s Return on Equity '
                     f'is forecast to be low in 3 years time ({formatted_future_roe_3y}).',
        }
