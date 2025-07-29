from apps.statements import types
from apps.statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class ShortTermLiabilitiesCheck(BaseCheck):
    def check(self) -> None:
        if self.company_short_term_assets > self.company_short_term_liabilities:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_short_term_assets = self.get_finance_format_with_unit(self.company_short_term_assets)
        formatted_short_term_liabilities = self.get_finance_format_with_unit(self.company_short_term_liabilities)

        self.descriptions = {
            'success': f'{formatted_slug}\'s short term assets '
                       f'({formatted_short_term_assets}) exceed '
                       f'its short term liabilities ({formatted_short_term_liabilities}).',
            'error': f'{formatted_slug}\'s short term assets '
                     f'({formatted_short_term_assets}) do not cover '
                     f'its short term liabilities ({formatted_short_term_liabilities}).',
        }


class LongTermLiabilitiesCheck(BaseCheck):
    def check(self) -> None:
        if self.company_short_term_assets > self.company_long_term_liabilities:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_short_term_assets = self.get_finance_format_with_unit(self.company_short_term_assets)
        formatted_long_term_liabilities = self.get_finance_format_with_unit(self.company_long_term_liabilities)

        self.descriptions = {
            'success': f'{formatted_slug}\'s short term assets '
                       f'({formatted_short_term_assets}) exceed '
                       f'its long term liabilities ({formatted_long_term_liabilities}).',
            'error': f'{formatted_slug}\'s short term assets '
                     f'({formatted_short_term_assets}) do not cover '
                     f'its long term liabilities ({formatted_long_term_liabilities}).',
        }


class DebtLevelCheck(BaseCheck):
    def check(self) -> None:
        if self.company_net_debt_to_equity_ratio > 0.02:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_net_debt_to_equity_ratio = self.get_percent_format(self.company_net_debt_to_equity_ratio)

        self.descriptions = {
            'success': f'{formatted_slug}\'s '
                       f'net debt to equity ratio ({formatted_net_debt_to_equity_ratio}) '
                       f'is considered satisfactory.',
            'error': f'{formatted_slug}\'s '
                     f'net debt to equity ratio ({formatted_net_debt_to_equity_ratio}) '
                     f'is not considered satisfactory.',
        }


class ReducingDebtCheck(BaseCheck):
    def check(self) -> None:
        if self.company_debt_to_equity_ratio_5Y_ago > self.company_debt_to_equity_ratio:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_debt_to_equity_ratio = self.get_percent_format(self.company_debt_to_equity_ratio)
        formatted_debt_to_equity_ratio_5y_ago = self.get_percent_format(self.company_debt_to_equity_ratio_5Y_ago)

        self.descriptions = {
            'success': f'{formatted_slug}\'s '
                       f'debt to equity ratio has reduced from {formatted_debt_to_equity_ratio_5y_ago} '
                       f'to {formatted_debt_to_equity_ratio} over the past 5 years.',
            'error': f'{formatted_slug}\'s '
                     f'debt to equity ratio has increased from {formatted_debt_to_equity_ratio_5y_ago} '
                     f'to {formatted_debt_to_equity_ratio} over the past 5 years.',
        }


class DebtCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.company_operating_cash_flow > self.company_debt:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_operating_cash_flow = self.get_percent_format(self.company_operating_cash_flow / self.company_debt)

        self.descriptions = {
            'success': f'{formatted_slug}\'s debt '
                       f'is well covered by operating cash flow ({formatted_operating_cash_flow}).',
            'error': f'{formatted_slug}\'s operating cash flow is negative, therefore debt is not well covered.',
        }


class InterestCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.company_ebit > self.company_interest_rate:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_debt_coverage = self.get_multiple_format(self.company_ebit / self.company_debt)

        self.descriptions = {
            'success': f'{formatted_slug} earns more interest than it pays, '
                       f'so coverage of interest payments is not a concern.',
            'error': f'{self.slug.upper()}\'s debt '
                     f'not is covered by EBIT ({formatted_debt_coverage} coverage).',
        }
