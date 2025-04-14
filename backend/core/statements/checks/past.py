from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class QualityEarningsCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasHighQualityPastEarnings',
            title='Quality Earnings',
            description='',
            question=f'Does {self.slug.upper()} have high quality earnings?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        self.descriptions = {
            'success': f'{self.slug.upper()} has high quality earnings.',
            'error': f'{self.slug.upper()} is currently unprofitable.',
        }


class GrowingProfitMarginCheck(BaseCheck):
    def check(self) -> None:
        if self.company_profit_margins > self.past_profit_margins:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasPastNetProfitMarginImprovedOverLastYear',
            title='Growing Profit Margin',
            description='',
            question=f'Have profit margins improved over the past year?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_profit_margins = self.get_percent_format(self.company_profit_margins)
        formatted_past_profit_margins = self.get_percent_format(self.past_profit_margins)

        self.descriptions = {
            'success': f'{formatted_slug}\'s '
                       f'current net profit margins ({formatted_profit_margins}) '
                       f'are higher than last year ({formatted_past_profit_margins}).',
            'error': f'{formatted_slug}\'s '
                     f'current net profit margins ({formatted_profit_margins}) '
                     f'are lower than last year ({formatted_past_profit_margins}).',
        }


class EarningsTrendCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings_growth_5y > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasGrownProfitsOverPast5Years',
            title='Earnings Trend',
            description='',
            question=f'Is {self.slug.upper()}\'s grown profits over the past 5 years?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_earnings_growth_5y = self.get_percent_format(self.company_earnings_growth_5y)

        self.descriptions = {
            'success': f'{formatted_slug}\'s earnings have grown by '
                       f'{formatted_earnings_growth_5y} per year over the past 5 years.',
            'error': f'{formatted_slug} is unprofitable, and losses have increased '
                     f'over the past 5 years at a rate of {formatted_earnings_growth_5y} per year.',
        }


class AcceleratingGrowthCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings_growth > self.company_earnings_growth_5y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasProfitGrowthAccelerated',
            title='Accelerating Growth',
            description='',
            question=f'Is {self.slug.upper()}\'s profit growth over the past year above its 5-year average?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_earnings_growth = self.get_percent_format(self.company_earnings_growth)
        formatted_earnings_growth_5y = self.get_percent_format(self.company_earnings_growth_5y)

        self.descriptions = {
            'success': f'{formatted_slug}\'s earnings growth over the past year '
                       f'({formatted_earnings_growth}) exceeds its 5-year average '
                       f'({formatted_earnings_growth_5y} per year).',
            'error': f'{formatted_slug}\'s earnings growth over the past year '
                       f'({formatted_earnings_growth}) is below than its 5-year average '
                       f'({formatted_earnings_growth_5y} per year).',
        }


class EarningsVsIndustryCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings_growth > self.industry_earnings_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGrowingFasterThanIndustry',
            title='Earnings vs Industry',
            description='',
            question=f'Is {self.slug.upper()} growing profit faster than the industry average?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_earnings_growth = self.get_percent_format(self.company_earnings_growth)
        formatted_industry_earnings_growth = self.get_percent_format(self.industry_earnings_growth)
        formatted_sector_name = self.sector_company_name.capitalize()

        self.descriptions = {
            'success': f'{formatted_slug} earnings growth over the past year '
                       f'({formatted_earnings_growth}) exceeded '
                       f'the {formatted_sector_name} industry {formatted_industry_earnings_growth}.',
            'error': f'{formatted_slug} earnings growth over the past year '
                       f'({formatted_earnings_growth}) was below than '
                       f'the {formatted_sector_name} industry {formatted_industry_earnings_growth}.',
        }


class HighROECheck(BaseCheck):
    def check(self) -> None:
        if self.company_roe > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsReturnOnEquityAboveThreshold',
            title='High ROE',
            description='',
            question=f'Is {self.slug.upper()}\'s return on equity above 20%?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_roe = self.get_percent_format(self.company_roe)

        self.descriptions = {
            'success': f'{formatted_slug}\'s Return on Equity ({formatted_roe}) is considered high.',
            'error': f'{formatted_slug}\'s Return on Equity ({formatted_roe}) is considered low.',
        }


class StableSharePriceCheck(BaseCheck):
    def check(self) -> None:
        if self.volatility_3m < self.sector_market_volatility_3m:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasPriceStability',
            title='Stable Share Price',
            description='',
            question=f'Has {self.slug.upper()} had a stable share price over the past 3 months?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1003,
        )
        slug = self.slug.upper()

        self.descriptions = {
            'success': f'{slug} has not had significant price volatility in the past 3 months.',
            'error': f'{slug}\' share price has been volatile over the past 3 months',
        }


class VolatilityOverTimeCheck(BaseCheck):
    def check(self) -> None:
        if self.volatility_1y < self.volatility_1y_past_year:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasReturnsVolatilityImprovedOverPastYear',
            title='Volatility Over Time',
            description='',
            question=f'Has {self.slug.upper()}\' volatility of returns improved over the past year?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1003,
        )
        slug = self.slug.upper()
        volatility_1y = self.get_percent_format(self.volatility_1y)
        volatility_1y_past_year = self.get_percent_format(self.volatility_1y_past_year)

        self.descriptions = {
            'success': f'{slug}\'s weekly volatility (7%) has been stable over the past year.',
            'error': f'{slug}\'s weekly volatility has increased '
                     f'from {volatility_1y_past_year} to {volatility_1y} over the past year.',
        }
