from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class ShortTermLiabilitiesCheck(BaseCheck):
    def check(self) -> None:
        if self.short_term_assets > self.short_term_liabilities:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='AreShortTermLiabilitiesCovered',
            title='Short Term Liabilities',
            description='',
            question=f'Are {self.slug.upper()}\'s short term liabilities covered by its cash and liquid assets?',
            level=level.GLOBAL,
            area=area.HEALTH,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s short term assets '
                       f'({self.short_term_assets}) exceed '
                       f'its short term liabilities ({self.short_term_liabilities}).',
            'error': f'{self.slug.upper()}\'s short term assets '
                     f'({self.short_term_assets}) do not cover '
                     f'its short term liabilities ({self.short_term_liabilities}).',
        }


class LongTermLiabilitiesCheck(BaseCheck):
    def check(self) -> None:
        if self.short_term_assets > self.long_term_liabilities:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='AreLongTermLiabilitiesCovered',
            title='Long Term Liabilities',
            description='',
            question=f'Are {self.slug.upper()}\'s long term liabilities covered by its cash and liquid assets?',
            level=level.GLOBAL,
            area=area.HEALTH,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s short term assets '
                       f'({self.short_term_assets}) exceed '
                       f'its long term liabilities ({self.short_term_liabilities}).',
            'error': f'{self.slug.upper()}\'s short term assets '
                     f'({self.short_term_assets}) do not cover '
                     f'its long term liabilities ({self.short_term_liabilities}).',
        }


class DebtLevelCheck(BaseCheck):
    def check(self) -> None:
        if self.debt_to_equity_ratio > 0.02:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDebtLevelAppropriate',
            title='Debt Level',
            description='',
            question=f'Is {self.slug.upper()}\'s debt level appropriate?',
            level=level.GLOBAL,
            area=area.HEALTH,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s '
                       f'net debt to equity ratio ({self.debt_to_equity_ratio}%) '
                       f'is considered satisfactory.',
            'error': f'{self.slug.upper()}\'s '
                       f'net debt to equity ratio ({self.debt_to_equity_ratio}%) '
                       f'is not considered satisfactory.',
        }


class ReducingDebtCheck(BaseCheck):
    def check(self) -> None:
        if self.debt_5Y_ago > self.debt:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasDebtReducedOverTime',
            title='Reducing Debt',
            description='',
            question=f'Has {self.slug.upper()}\'s debt reduced over time?',
            level=level.GLOBAL,
            area=area.HEALTH,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s '
                       f'debt to equity ratio has reduced from {self.debt_5Y_ago*100}% '
                       f'to {self.debt*100}% over the past 5 years.',
            'error': f'{self.slug.upper()}\'s '
                     f'debt to equity ratio has increased from {self.debt_5Y_ago*100}% '
                     f'to {self.debt*100}% over the past 5 years.',
        }


class DebtCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.operating_cash_flow > self.debt:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDebtCoveredByCashflow',
            title='Debt Coverage',
            description='',
            question=f'Is {self.slug.upper()}\'s debt covered by its cash flow?',
            level=level.GLOBAL,
            area=area.HEALTH,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s operating cash flow is negative, therefore debt is not well covered.',
            'error': f'{self.slug.upper()}\'s debt '
                     f'is well covered by operating cash flow ({self.operating_cash_flow / self.debt * 100}%).',
        }


class InterestCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.company_ebit > self.interest_rate:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsInterestCoveredByProfit',
            title='Interest Coverage',
            description='',
            question=f'Is {self.slug.upper()}\'s interest expenses covered by its profits?',
            level=level.GLOBAL,
            area=area.HEALTH,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()} earns more interest than it pays, '
                       f'so coverage of interest payments is not a concern.',
            'error': f'{self.slug.upper()}\'s debt '
                     f'not is covered by EBIT ({self.company_ebit / self.debt}x coverage).',
        }
