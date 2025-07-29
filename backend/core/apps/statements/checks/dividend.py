from apps.statements import types
from apps.statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class SignificantDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.company_dividend_yield > self.market_dividend_yield_p25:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDividendSignificant',
            title='Notable Dividend',
            description='',
            question=f'Is {self.slug.upper()}\'s dividend yield above the bottom 25% of dividend payers?',
            level=level.GLOBAL,
            area=area.DIVIDENDS,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_country_adjectif = self.market_country_adjectif.capitalize()
        formatted_dividend_yield = self.get_percent_format(self.company_dividend_yield)
        formatted_market_dividend_yield_p25 = self.get_percent_format(self.market_dividend_yield_p25)

        self.descriptions = {
            'success': f'{formatted_slug}\'s dividend ({formatted_dividend_yield}) is higher than '
                       f'the bottom 25% of dividend payers in '
                       f'the {formatted_country_adjectif} market '
                       f'({formatted_market_dividend_yield_p25}).',
            'error': f'{formatted_slug}\'s dividend ({formatted_dividend_yield}) is lower than '
                     f'the bottom 25% of dividend payers in '
                     f'the {formatted_country_adjectif} market '
                     f'({formatted_market_dividend_yield_p25}).',
        }


class HighDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.company_dividend_yield > self.market_dividend_yield_p75:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDividendYieldTopTier',
            title='High Dividend',
            description='',
            question=f'Is {self.slug.upper()}\'s dividend yield in the top 25% of dividend payers?',
            level=level.GLOBAL,
            area=area.DIVIDENDS,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_country_adjectif = self.market_country_adjectif.capitalize()
        formatted_dividend_yield = self.get_percent_format(self.company_dividend_yield)
        formatted_market_dividend_yield_p75 = self.get_percent_format(self.market_dividend_yield_p75)

        self.descriptions = {
            'success': f'{formatted_slug}\'s dividend '
                       f'({formatted_dividend_yield}) is in the top 25% of dividend payers in '
                       f'the {formatted_country_adjectif} market '
                       f'({formatted_market_dividend_yield_p75})',
            'error': f'{formatted_slug}\'s dividend '
                     f'({formatted_dividend_yield}) is low compared to the top 25% of dividend payers in '
                     f'the {formatted_country_adjectif} market '
                     f'({formatted_market_dividend_yield_p75}).',
        }


class StableDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.company_dividend_is_volatile_in_10y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDividendStable',
            title='Stable Dividend',
            description='',
            question=f'Is {self.slug.upper()}\'s dividend stable?',
            level=level.GLOBAL,
            area=area.DIVIDENDS,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        self.descriptions = {
            'success': f'{self.slug.upper()}\'s dividends per share have been stable in the past 10 years.',
            'error': f'{self.slug.upper()}\'s dividend payments have been volatile in the past 10 years.',
        }


class GrowingDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.company_dividend_amount > self.company_dividend_amount_10y_ago:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDividendGrowing',
            title='Growing Dividend',
            description='',
            question=f'Is {self.slug.upper()}\'s dividend growing over the long-term?',
            level=level.GLOBAL,
            area=area.DIVIDENDS,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        self.descriptions = {
            'success': f'{self.slug.upper()}\'s dividend payments have increased over the past 10 years.',
            'error': f'{self.slug.upper()}\'s dividend payments have declined over the past 10 years.',
        }


class EarningsCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.company_payout_ratio < 1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDividendCovered',
            title='Earnings Coverage',
            description='',
            question=f'Is {self.slug.upper()}\'s dividend covered by earnings?',
            level=level.GLOBAL,
            area=area.DIVIDENDS,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_payout_ratio = self.get_percent_format(self.company_payout_ratio)

        self.descriptions = {
            'success': f'With its reasonably low payout ratio ({formatted_payout_ratio}), '
                       f'{formatted_slug}\'s dividend payments are well covered by earnings.',
            'error': f'With its high payout ratio ({formatted_payout_ratio}), '
                     f'{formatted_slug}\'s dividend payments are not well covered by earnings',
        }


class CashFlowCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.company_cash_payout_ratio < 1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDividendCoveredByFreeCashFlow',
            title='Cash Flow Coverage',
            description='',
            question=f'Is {self.slug.upper()}\'s dividend covered by free cash flows?',
            level=level.GLOBAL,
            area=area.DIVIDENDS,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1002,
        )
        formatted_slug = self.slug.upper()
        formatted_payout_ratio = self.get_percent_format(self.company_cash_payout_ratio)

        self.descriptions = {
            'success': f'With its reasonably low payout ratio ({formatted_payout_ratio}), '
                       f'{formatted_slug}\'s dividend payments are well covered by cash flows.',
            'error': f'With its high cash payout ratio ({formatted_payout_ratio}), '
                     f'{formatted_slug}\'s dividend payments are not well covered by cash flows.',
        }
