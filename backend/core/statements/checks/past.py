from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class QualityEarningsCheck(BaseCheck):
    def check(self) -> None:
        if self.net_income > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'{self.slug.upper()} has high quality earnings.',
            'error': f'{self.slug.upper()} is currently unprofitable.',
        }


class GrowingProfitMarginCheck(BaseCheck):
    def check(self) -> None:
        if self.profit_margins > self.past_profit_margins:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s '
                       f'current net profit margins ({self.profit_margins*100}%) '
                       f'are higher than last year ({self.past_profit_margins*100}%).',
            'error': f'{self.slug.upper()}\'s '
                     f'current net profit margins ({self.profit_margins*100}%) '
                     f'are lower than last year ({self.past_profit_margins*100}%).',
        }


class EarningsTrendCheck(BaseCheck):
    def check(self) -> None:
        if self.net_income_growth_5y > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s earnings have grown by '
                       f'{self.net_income_growth_5y*100}% per year over the past 5 years.',
            'error': f'{self.slug.upper()} is unprofitable, and losses have increased '
                     f'over the past 5 years at a rate of {self.net_income_growth_5y*100}% per year.',
        }


class AcceleratingGrowthCheck(BaseCheck):
    def check(self) -> None:
        if self.earnings_growth > self.net_income_growth_5y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s earnings growth over the past year '
                       f'({self.earnings_growth*100}%) exceeds its 5-year average '
                       f'({self.net_income_growth_5y*100}% per year).',
            'error': f'{self.slug.upper()}\'s earnings growth over the past year '
                       f'({self.earnings_growth*100}%) is below than its 5-year average '
                       f'({self.net_income_growth_5y*100}% per year).',
        }


class EarningsVsIndustryCheck(BaseCheck):
    def check(self) -> None:
        if self.earnings_growth > self.industry_earnings_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'{self.slug.upper()} earnings growth over the past year '
                       f'({self.earnings_growth}%) exceeded '
                       f'the {self.company_sector_name.capitalize()} industry {self.industry_earnings_growth}%.',
            'error': f'{self.slug.upper()} earnings growth over the past year '
                       f'({self.earnings_growth}%) was below than '
                       f'the {self.company_sector_name.capitalize()} industry {self.industry_earnings_growth}%.',
        }


class HighROECheck(BaseCheck):
    def check(self) -> None:
        if self.company_roe > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGrowingFasterThanIndustry',
            title='High ROE',
            description='',
            question=f'Is {self.slug.upper()}\'s return on equity above 20%?',
            level=level.GLOBAL,
            area=area.PAST,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s Return on Equity ({self.company_roe*100}%) is considered high.',
            'error': f'{self.slug.upper()}\'s Return on Equity ({self.company_roe*100}%) is considered low.',
        }
