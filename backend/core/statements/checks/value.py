from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class BelowFairValueCheck(BaseCheck):
    def check(self) -> None:
        if self.current_price < self.fair_price:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsUndervaluedBasedOnDCF',
            title='Below Fair Value',
            description='',
            question=f'Is {self.slug.upper()} moderately undervalued based on cash flows?',
            level=level.GLOBAL,
            area=area.VALUE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()} ({self.current_price}) '
                       f'is trading below our estimate of fair value ({self.fair_price})',
            'error': f'{self.slug.upper()} ({self.current_price}) '
                     f'is trading above our estimate of fair value ({self.fair_price})',
        }


class SignificantlyBelowFairValueCheck(BaseCheck):
    def check(self) -> None:
        if (self.current_price - self.fair_price) / self.fair_price > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsHighlyUndervaluedBasedOnDCF',
            title='Significantly Below Fair Value',
            description='',
            question=f'Is {self.slug.upper()} substantially undervalued based on cash flows?',
            level=level.GLOBAL,
            area=area.VALUE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()} ({self.current_price}) is trading below fair value by more than 20%.',
            'error': f'{self.slug.upper()} ({self.current_price}) is trading above our estimate of fair value.',
        }


class PriceToEarningsVsPeersCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.peers_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGoodValueComparingPriceToEarningsToPeersAverageValue',
            title='Price-To-Earnings vs Peers',
            description='',
            question=f'Is {self.slug.upper()} considered good value compared to its peers?',
            level=level.GLOBAL,
            area=area.VALUE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()} is good value based on its Price-To-Earnings Ratio '
                       f'({self.company_pe}x) compared to the peer average ({self.peers_pe}x).',
            'error': f'{self.slug.upper()} is expensive based on its Price-To-Earnings Ratio '
                     f'({self.company_pe}x) compared to the peer average ({self.peers_pe}x).',
        }


class PriceToEarningsVsIndustryCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.industry_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGoodValueComparingPriceToEarningsToIndustry',
            title='Price-To-Earnings vs Industry',
            description='',
            question=f'Is {self.slug.upper()} considered good value compared to its industry?',
            level=level.GLOBAL,
            area=area.VALUE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()} is good value based on its Price-To-Earnings Ratio '
                       f'({self.company_pe}x) compared to the European Banks industry average ({self.industry_pe}x).',
            'error': f'{self.slug.upper()} is expensive based on its Price-To-Earnings Ratio '
                     f'({self.company_pe}x) compared to the US Semiconductor industry average ({self.industry_pe}x).',
        }


class PriceToEarningsVsFairRatioCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.fair_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.description['success']
        else:
            self.statement['description'] = self.description['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGoodValueComparingRatioToFairRatio',
            title='Price-To-Earnings vs Fair Ratio',
            description='',
            question=f'Is {self.slug.upper()} considered good value compared to its fair ratio?',
            level=level.GLOBAL,
            area=area.VALUE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.description = {
            'success': f'{self.slug.upper()} is good value based on its Price-To-Earnings Ratio '
                       f'({self.company_pe}x) '
                       f'compared to the estimated Fair Price-To-Earnings Ratio ({self.fair_pe}x).',
            'error': f'{self.slug.upper()} is expensive based on its Price-To-Earnings Ratio '
                     f'({self.company_pe}x) '
                     f'compared to the estimated Fair Price-To-Earnings Ratio ({self.fair_pe}x).',
        }
