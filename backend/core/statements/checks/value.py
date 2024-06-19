from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class BelowFairValueCheck(BaseCheck):
    def check(self) -> None:
        if self.company_current_price < self.company_fair_price:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_current_price = self.get_finance_format(self.company_current_price)
        formatted_fair_price = self.get_finance_format(self.company_current_price)

        self.descriptions = {
            'success': f'{formatted_slug} '
                       f'({formatted_current_price}) '
                       f'is trading below our estimate of fair value '
                       f'({formatted_fair_price})',
            'error': f'{formatted_slug} '
                     f'({formatted_current_price}) '
                     f'is trading above our estimate of fair value '
                     f'({formatted_fair_price})',
        }


class SignificantlyBelowFairValueCheck(BaseCheck):
    def check(self) -> None:
        if (self.company_current_price - self.company_fair_price) / self.company_fair_price > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_current_price = self.get_finance_format(self.company_current_price)

        self.descriptions = {
            'success': f'{formatted_slug} ({formatted_current_price}) is trading below fair value '
                       f'by more than 20%.',
            'error': f'{formatted_slug} ({formatted_current_price}) is trading above our estimate of fair value.',
        }


class PriceToEarningsVsPeersCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.peers_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_pe = self.get_multiple_format(self.company_pe)
        formatted_peers_pe = self.get_multiple_format(self.peers_pe)

        self.descriptions = {
            'success': f'{formatted_slug} is good value based on its Price-To-Earnings Ratio '
                       f'({formatted_pe}) compared to the peer average ({formatted_peers_pe}).',
            'error': f'{formatted_slug} is expensive based on its Price-To-Earnings Ratio '
                     f'({formatted_pe}) compared to the peer average ({formatted_peers_pe}).',
        }


class PriceToEarningsVsIndustryCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.industry_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        country_adjectif = self.market_country_adjectif.capitalize()
        sector_name = self.sector_company_name.capitalize()
        formatted_pe = self.get_multiple_format(self.company_pe)
        formatted_industry_pe = self.get_multiple_format(self.industry_pe)

        self.descriptions = {
            'success': f'{formatted_slug} is good value based on its Price-To-Earnings Ratio '
                       f'({formatted_pe}) compared to the '
                       f'{country_adjectif} {sector_name} industry average ({formatted_industry_pe}).',
            'error': f'{formatted_slug} is expensive based on its Price-To-Earnings Ratio '
                     f'({formatted_pe}) compared to the '
                     f'{country_adjectif} {sector_name} industry average ({formatted_industry_pe}).',
        }


class PriceToEarningsVsFairRatioCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.company_fair_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['description'] = self.descriptions['error']

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
        formatted_slug = self.slug.upper()
        formatted_pe = self.get_multiple_format(self.company_pe)
        formatted_fair_pe = self.get_multiple_format(self.company_fair_pe)

        self.descriptions = {
            'success': f'{formatted_slug} is good value based on its Price-To-Earnings Ratio '
                       f'({formatted_pe}) '
                       f'compared to the estimated Fair Price-To-Earnings Ratio ({formatted_fair_pe}).',
            'error': f'{formatted_slug} is expensive based on its Price-To-Earnings Ratio '
                     f'({formatted_pe}) '
                     f'compared to the estimated Fair Price-To-Earnings Ratio ({formatted_fair_pe}).',
        }


class ReturnVsIndustryCheck(BaseCheck):
    def check(self) -> None:
        if self.return_1y < self.sector_market_return_1y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='Is1YearReturnInLineOrAboveIndustry',
            title='Return vs Industry',
            description='',
            question=f'Is {self.slug.upper()}\'s 1 year returns above the industry?',
            level=level.GLOBAL,
            area=area.VALUE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        slug = self.slug.upper()
        country_adjectif = self.market_country_adjectif.capitalize()
        sector_name = self.sector_company_name.capitalize()
        sector_market_return_1y = self.get_percent_format(self.sector_market_return_1y)

        self.descriptions = {
            'success': f'{slug} exceeded the {country_adjectif} {sector_name} industry which returned'
                       f' {sector_market_return_1y} over the past year.',
            'error': f'{slug} underperformed the {country_adjectif} {sector_name} industry which returned'
                     f' {sector_market_return_1y} over the past year.',
        }


class ReturnVsMarketCheck(BaseCheck):
    def check(self) -> None:
        if self.return_1y < self.market_return_1y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='Is1YearReturnInLineOrAboveMarket',
            title='Return vs Market',
            description='',
            question=f'Is {self.slug.upper()}\'s 1 year returns above the market?',
            level=level.GLOBAL,
            area=area.VALUE,
            type=type_.STATEMENTS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        slug = self.slug.upper()
        country_adjectif = self.market_country_adjectif.capitalize()
        market_return_1y = self.get_percent_format(self.market_return_1y)

        self.descriptions = {
            'success': f'{slug} exceeded the {country_adjectif} Market which returned'
                       f' {market_return_1y} over the past year.',
            'error': f'{slug} underperformed the {country_adjectif} Market which returned'
                     f' {market_return_1y} over the past year.',
        }
