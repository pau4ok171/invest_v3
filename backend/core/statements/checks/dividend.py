from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class NotableDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.dividend_yield > self.market_dividend_yield_p25:
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
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s dividend ({self.dividend_yield * 100}%) is higher than '
                       f'the bottom 25% of dividend payers in '
                       f'the {self.market_country_adjectif.capitalize()} market '
                       f'({self.market_dividend_yield_p25 * 100}%).',
            'error': f'{self.slug.upper()}\'s dividend ({self.dividend_yield * 100}%) is lower than '
                     f'the bottom 25% of dividend payers in '
                     f'the {self.market_country_adjectif.capitalize()} market '
                     f'({self.market_dividend_yield_p25 * 100}%).',
        }


class HighDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.dividend_yield > self.market_dividend_yield_p75:
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
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s dividend '
                       f'({self.dividend_yield*100}%) is in the top 25% of dividend payers in '
                       f'the {self.market_country_adjectif.capitalize()} market '
                       f'({self.market_dividend_yield_p75*100}%)',
            'error': f'{self.slug.upper()}\'s dividend '
                     f'({self.dividend_yield*100}%) is low compared to the top 25% of dividend payers in '
                     f'the {self.market_country_adjectif.capitalize()} market '
                     f'({self.market_dividend_yield_p75*100}%).',
        }


class StableDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.dividend_is_volatile_in_10y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s dividends per share have been stable in the past 10 years.',
            'error': f'{self.slug.upper()}\'s dividend payments have been volatile in the past 10 years.',
        }


class GrowingDividendCheck(BaseCheck):
    def check(self) -> None:
        if self.dividend_amount > self.dividend_amount_10y_ago:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'{self.slug.upper()}\'s dividend payments have increased over the past 10 years.',
            'error': f'{self.slug.upper()}\'s dividend payments have declined over the past 10 years.',
        }


class EarningsCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.payout_ratio < 1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'With its reasonably low payout ratio ({self.payout_ratio*100}%), '
                       f'{self.slug.upper()}\'s dividend payments are well covered by earnings.',
            'error': f'With its high payout ratio ({self.payout_ratio*100}%), '
                     f'{self.slug.upper()}\'s dividend payments are not well covered by earnings',
        }


class CashFlowCoverageCheck(BaseCheck):
    def check(self) -> None:
        if self.cash_payout_ratio < 1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

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
        )
        self.description = {
            'success': f'With its reasonably low payout ratio ({self.payout_ratio * 100}%), '
                       f'{self.slug.upper()}\'s dividend payments are well covered by cash flows.',
            'error': f'With its high cash payout ratio ({self.payout_ratio * 100}%), '
                     f'{self.slug.upper()}\'s dividend payments are not well covered by cash flows.',
        }
