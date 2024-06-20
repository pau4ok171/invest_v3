from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


class HasFinancialDataCheck(BaseCheck):
    def check(self) -> None:
        if self.company_object.reports.exists():
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasFinancialData',
            title='Has Financial Data',
            description='',
            question=f'Does {self.slug.upper()} have financial data available?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.descriptions = {
            'success': f'{self.slug.upper()} has financial data available.',
            'error': f'{self.slug.upper()} has\'t financial data available.',
        }


class HasBeenGrowingProfitOrRevenueCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings_growth > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasBeenGrowingProfitOrRevenue',
            title='Has Been Growing Profit Or Revenue',
            description='',
            question=f'Has {self.slug.upper()} been growing?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        earnings_growth_1y = self.get_percent_format(self.company_earnings_growth)

        self.descriptions = {
            'success': f'Earnings grew by {earnings_growth_1y} over the past year',
            'error': f'Earnings decreased by {earnings_growth_1y} over past year',
        }


class IsDividendAttractiveCheck(BaseCheck):
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
            name='IsDividendAttractive',
            title='Is Dividend Attractive',
            description='',
            question=f'Is {self.slug.upper()}\'s dividend attractive?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        company_payout_ratio = self.get_percent_format(self.company_payout_ratio)

        self.descriptions = {
            'success': f'Pays a reliable dividend of {company_payout_ratio}',
            'error': f'{self.slug.upper()} has cut its dividend at least once in the past',
        }


class IsGoodRelativeValueCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.peers_pe and self.company_pe < self.industry_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGoodRelativeValue',
            title='Is Good Relative Value',
            description='',
            question=f'Is {self.slug.upper()} trading at good relative value?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.descriptions = {
            'success': f'Trading at good value compared to peers and industry',
            'error': f'Not trading at good value compared to peers and industry',
        }


class IsGoodValueCheck(BaseCheck):
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
            name='IsGoodValue',
            title='Is Good Value',
            description='',
            question=f'Is {self.slug.upper()} good value?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        value = (self.company_current_price - self.company_fair_price)/self.company_current_price
        formatted_value = self.get_percent_format(abs(value))
        self.descriptions = {
            'success': f'Trading at {formatted_value} below our estimate of its fair value.',
            'error': f'Trading at {formatted_value} above our estimate of its fair value.',
        }


class IsGoodValueComparedToIndustryCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.industry_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGoodValueComparedToIndustry',
            title='Is Good Value Compared To Industry',
            description='',
            question=f'Is {self.slug.upper()} good value vs. industry?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.descriptions = {
            'success': f'Trading at good value vs. industry average Price-To-Earnings ratio',
            'error': f'Not trading at good value vs. industry average Price-To-Earnings ratio',
        }


class IsGoodValueComparedToPeersCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.peers_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGoodValueComparedToPeers',
            title='Is Good Value Compared To Peers',
            description='',
            question=f'Is {self.slug.upper()} good value vs. peers?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.descriptions = {
            'success': f'Trading at good value vs. peer average Price-To-Earnings ratio',
            'error': f'Not trading at good value vs. peer average Price-To-Earnings ratio',
        }


class IsGrowingProfitOrRevenueCheck(BaseCheck):
    def check(self) -> None:
        if self.company_forecast_earnings_growth > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsGrowingProfitOrRevenue',
            title='Is Growing Profit Or Revenue',
            description='',
            question=f'Is {self.slug.upper()} growing?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        forecast_earnings_growth = self.get_percent_format(self.company_forecast_earnings_growth)

        self.descriptions = {
            'success': f'Earnings are forecast to grow {forecast_earnings_growth} per year',
            'error': f'Earnings are forecast to decrease {forecast_earnings_growth} per year',
        }


class IsTradingBelowAnalystPriceTargetsCheck(BaseCheck):
    def check(self) -> None:
        if self.company_current_price < self.average_price_target_1y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsTradingBelowAnalystPriceTargets',
            title='Is Trading Below Analyst Price Targets',
            description='',
            question=f'Are analysts in good agreement {self.slug.upper()} stock price will rise?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        value = (self.average_price_target_1y-self.company_current_price)/self.average_price_target_1y
        formatted_value = self.get_percent_format(value)
        self.descriptions = {
            'success': f'Analysts in good agreement that stock price will rise by {formatted_value}',
            'error': f'Analysts not in good agreement that stock price will rise.',
        }


class IsTradingBelowFairRatioCheck(BaseCheck):
    def check(self) -> None:
        if self.company_pe < self.company_fair_pe:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsTradingBelowFairRatio',
            title='Is Trading Below Fair Ratio',
            description='',
            question=f'Is {self.slug.upper()} trading below calculated fair ratio?',
            level=level.INIT,
            area=area.REWARDS,
            type=type_.REWARDS,
            status=status.FAIL,
            severity=severity.NONE,
        )
        self.descriptions = {
            'success': f'Trading below our calculated fair Price-To-Earnings ratio',
            'error': f'Not trading below our calculated fair Price-To-Earnings ratio',
        }
