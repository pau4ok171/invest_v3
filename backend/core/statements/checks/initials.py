from statements import types
from statements.checks.base import BaseCheck

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


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
            outcome=1001,
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
            outcome=1001,
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
            outcome=1001,
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
            outcome=1001,
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
            outcome=1001,
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
            outcome=1001,
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
            outcome=1001,
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
            outcome=1001,
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
            outcome=1001,
        )
        self.descriptions = {
            'success': f'Trading below our calculated fair Price-To-Earnings ratio',
            'error': f'Not trading below our calculated fair Price-To-Earnings ratio',
        }


class AreRevenueAndEarningsExpectedToGrowCheck(BaseCheck):
    def check(self) -> None:
        if self.earnings_growth_per_year_forecast_3y > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='AreRevenueAndEarningsExpectedToGrow',
            title='Are Revenue And Earnings Expected To Grow',
            description='',
            question=f'Are revenue and earnings forecast to grow?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )
        earnings_growth_per_year_forecast_3y = self.get_percent_format(self.earnings_growth_per_year_forecast_3y)

        self.descriptions = {
            'success': f'Earnings are forecast to grow by an average of {earnings_growth_per_year_forecast_3y} '
                       f'per year for the next 3 years',
            'error': f'Earnings are forecast to decrease by an average of {earnings_growth_per_year_forecast_3y} '
                     f'per year for the next 3 years',
        }


class HasCapitalisationRateIncreasedSignificantlyCheck(BaseCheck):
    def check(self) -> None:
        if (self.capitalisation_rate-self.capitalisation_rate_1y/self.capitalisation_rate) > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasCapitalisationRateIncreasedSignificantly',
            title='Has Capitalisation Rate Increased Significantly',
            description='',
            question=f'Has {self.slug.upper()}\'s capitalisation rate increased significantly over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )
        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasCashFromOperationGrownSlowerThanNetIncomeCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings_growth < self.operating_cash_flow_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasCashFromOperationsGrownSlowerThanNetIncome',
            title='Has Cash From Operations Grown Slower Than Net Income',
            description='',
            question=f'Has {self.slug.upper()}\'s Cash From Operations grown '
                     f'slower than net income over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )
        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasDecliningGrossProfitMarginsCheck(BaseCheck):
    def check(self) -> None:
        if self.gross_profit_margin > self.gross_profit_margin_1y:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasDecliningGrossProfitMargins',
            title='Has Declining Gross Profit Margins',
            description='',
            question=f'Have {self.slug.upper()}\'s gross profit margins fallen over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )
        gross_profit_margin = self.get_multiple_format(self.gross_profit_margin)
        gross_profit_margin_1y = self.get_multiple_format(self.gross_profit_margin_1y)

        self.descriptions = {
            'success': f'{self.slug.upper()}\'s gross profit margin has increased from '
                       f'{gross_profit_margin_1y} to {gross_profit_margin}',
            'error': f'{self.slug.upper()}\'s gross profit margin has decreased from '
                     f'{gross_profit_margin_1y} to {gross_profit_margin}',
        }


class HasDecliningProfitMarginsCheck(BaseCheck):
    def check(self) -> None:
        if self.company_profit_margins > self.past_profit_margins:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasDecliningProfitMargins',
            title='Has Declining Profit Margins',
            description='',
            question=f'Have {self.slug.upper()}\'s profit margins fallen over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )
        profit_margin = self.get_percent_format(self.company_profit_margins)
        profit_margin_1y = self.get_percent_format(self.past_profit_margins)

        self.descriptions = {
            'success': f'{self.slug.upper()}\'s profit margin has increased from {profit_margin_1y} to {profit_margin}',
            'error': f'{self.slug.upper()}\'s profit margin has decreased from {profit_margin_1y} to {profit_margin}',
        }


class HasFiledWithinMonthsCheck(BaseCheck):
    def check(self) -> None:
        if self.company_object.reports.exists():
            diff = self.get_report_diff()

            if diff.days < 180:

                self.statement['status'] = status.PASS
                self.statement['description'] = self.descriptions['success']
                self.statement['severity'] = severity.NONE
            else:
                self.statement['status'] = status.FAIL
                self.statement['description'] = self.descriptions['error']
                self.statement['severity'] = severity.MINOR

        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = 'No reports'
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasFiledWithin6Months',
            title='Has Filed Within Months',
            description='',
            question=f'Has {self.slug.upper()} filed financial statements in the past 6 months?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )
        diff = self.get_report_diff()

        if diff:
            self.descriptions = {
                'success': f'{self.slug.upper()} last filed financial statements {diff.days} days ago',
                'error': f'{self.slug.upper()} last filed financial statements {diff.days} days ago',
            }


class HasFiledWithinPastYearCheck(BaseCheck):
    def check(self) -> None:
        if self.company_object.reports.exists():
            diff = self.get_report_diff()

            if diff.days < 365:

                self.statement['status'] = status.PASS
                self.statement['description'] = self.descriptions['success']
                self.statement['severity'] = severity.NONE
            else:
                self.statement['status'] = status.FAIL
                self.statement['description'] = self.descriptions['error']
                self.statement['severity'] = severity.MINOR

        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = 'No reports'
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasFiledWithinPastYear',
            title='Has Filed Within Past Year',
            description='',
            question=f'Has {self.slug.upper()} filed financial statements in the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )
        diff = self.get_report_diff()

        if diff:
            self.descriptions = {
                'success': f'{self.slug.upper()} last filed financial statements {diff.days} days ago',
                'error': f'{self.slug.upper()} last filed financial statements {diff.days} days ago',
            }


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
            outcome=1001,
        )
        self.descriptions = {
            'success': f'{self.slug.upper()} has financial data available.',
            'error': f'{self.slug.upper()} has\'t financial data available.',
        }


class HasHighAccrualsRatioCheck(BaseCheck):
    def check(self) -> None:
        if abs(self.sloan_ratio) <= 0.10:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        elif abs(self.sloan_ratio <= 0.25):
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['high_error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasHighAccrualsRatio',
            title='Has High Accruals Ratio',
            description='',
            question=f'Does {self.slug.upper()} have a high accrual ratio?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
            'high-error': f'Dangerously high',
        }


class HasHighQualityEarningsCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasHighQualityEarnings',
            title='Has High Quality Earnings',
            description='',
            question=f'Do they have high quality earnings?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'The company’s earnings are high quality',
            'error': f'The company’s earnings are low quality',
        }


class HasInventoryGrownSignificantlyFasterThanSalesCheck(BaseCheck):
    def check(self) -> None:
        if self.sales_growth > self.inventory_growth:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasInventoryGrownSignificantlyFasterThanSales',
            title='Has Inventory Grown Significantly Faster Than Sales',
            description='',
            question=f'Have {self.slug.upper()}\'s inventories grown significantly '
                     f'faster than sales over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasLargeDecreaseInUnearnedRevenueCheck(BaseCheck):
    def check(self) -> None:
        if self.unearned_revenue_growth > -0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasLargeDecreaseInUnearnedRevenue',
            title='Has Large Decrease In Unearned Revenue',
            description='',
            question=f'Does {self.slug.upper()} have a large decrease in unearned revenue over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasLargeIncreaseInAccountsReceivableCheck(BaseCheck):
    def check(self) -> None:
        if self.accounts_receivable_growth > 0.2:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasLargeIncreaseInAccountsReceivable',
            title='Has Large Increase In Accounts Receivable',
            description='',
            question=f'Does {self.slug.upper()} have a large increase in accounts receivable over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasLargeNegativeOneTimeChargesCheck(BaseCheck):
    def check(self) -> None:
        if self.one_off_charges < 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasLargeNegativeOneTimeCharges',
            title='Has Large Negative One Time Charges',
            description='',
            question=f'Does {self.slug.upper()} suffer from significant negative one-off charges?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasLargeOneTimeChargesCheck(BaseCheck):
    def check(self) -> None:
        if abs(self.one_off_charges/self.company_earnings) > 0.1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasLargeOneTimeCharges',
            title='Has Large One Time Charges',
            description='',
            question=f'Is {self.slug.upper()} impacted by significant one-off charges?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasLargePositiveOneTimeChargesCheck(BaseCheck):
    def check(self) -> None:
        if self.one_off_charges > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasLargePositiveOneTimeCharges',
            title='Has Large Positive One Time Charges',
            description='',
            question=f'Does {self.slug.upper()} benefit from significant positive one-off charges?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasLargePositiveOneTimeChargesAndProfitableCheck(BaseCheck):
    def check(self) -> None:
        if self.one_off_charges > 0 and self.company_earnings > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasLargePositiveOneTimeChargesAndProfitable',
            title='Has Large Positive One Time Charges And Profitable',
            description='',
            question=f'Is {self.slug.upper()}\'s reported profit improved by significant one-off charges?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasMeaningfulMarketCapCheck(BaseCheck):
    """
    MegaCap: > 200B$
    LargeCap: > 10B$
    MidCap: > 2B$
    SmallCap: > 0.3B$
    MicroCap: > 0.05B$
    NanoCap: > 0B$
    """
    def check(self) -> None:
        if self.market_cap_usd > 2_000_000_000:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasMeaningfulMarketCap',
            title='Has Meaningful Market Cap',
            description='',
            question=f'Do they have a meaningful market capitalization?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )
        market_cap = self.get_finance_format_with_unit(self.market_cap)

        self.descriptions = {
            'success': f'Market cap is meaningful ({market_cap})',
            'error': f'Market cap is not meaningful ({market_cap})',
        }


class HasMeaningfulRevenueCheck(BaseCheck):
    def check(self) -> None:
        if self.revenue / self.market_cap > 0.1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasMeaningfulRevenue',
            title='Has Meaningful Revenue',
            description='',
            question=f'Do they have meaningful levels of revenue?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )
        revenue = self.get_finance_format_with_unit(self.revenue)

        self.descriptions = {
            'success': f'Revenue is meaningful ({revenue})',
            'error': f'Revenue is not meaningful ({revenue})',
        }


class HasNegativeGrossMarginCheck(BaseCheck):
    def check(self) -> None:
        if self.gross_profit_margin > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasNegativeGrossMargin',
            title=f'Has Negative Gross Margin',
            description='',
            question=f'Does {self.slug.upper()} have negative gross margin?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'{self.slug.upper()}\'s gross profit margin is {self.gross_profit_margin:.5f}',
            'error': f'{self.slug.upper()}\'s gross profit margin is {self.gross_profit_margin:.5f}',
        }


class HasNetProfitMarginImprovedOverPastYearCheck(BaseCheck):
    def check(self) -> None:
        if self.company_profit_margins > self.past_profit_margins or self.company_profit_margins > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasNetProfitMarginImprovedOverPastYear',
            title='Has Net Profit Margin Improved Over Past Year',
            description='',
            question=f'Have profit margins improved over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Profit margins improved or {self.slug.upper()} became profitable',
            'error': f'Insufficient data or unprofitable',
        }


class HasNoConcerningRecentEventsCheck(BaseCheck):
    def check(self) -> None:
        if self.events_was_occurred:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasNoConcerningRecentEvents',
            title='Has No Concerning Recent Events',
            description='',
            question=f'Are there any concerning recent events?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'No concerning events detected',
            'error': f'Concerning events detected',
        }


class HasNoSubstantialInsiderSellingOverPastQuarterCheck(BaseCheck):
    def check(self) -> None:
        if not self.substantial_insider_selling_was_occurred:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasNoSubstantialInsiderSellingOverPastQuarter',
            title='Has No Substantial Insider Selling Over Past Quarter',
            description='',
            question=f'Has there been substantial insider selling in the past 3 months?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasNotDilutedOverPastYearCheck(BaseCheck):
    def check(self) -> None:
        if not self.has_diluted_over_past_year:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasNotDilutedOverPastYear',
            title='Has Not Diluted Over Past Year',
            description='',
            question=f'Have shareholders been diluted over the past year?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )

        self.descriptions = {
            'success': f'Shareholders have not been meaningfully diluted in the past year or recently listed',
            'error': f'Shareholders have been meaningfully diluted in the past year or recently listed',
        }


class HasSignificantNonOperatingRevenueCheck(BaseCheck):
    def check(self) -> None:
        if self.non_operating_revenue < self.operating_revenue:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasSignificantNonOperatingRevenue',
            title='Has Significant Non Operating Revenue',
            description='',
            question=f'Does {self.slug.upper()} have significant non-operating revenue?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasStableSharePriceCheck(BaseCheck):
    def check(self) -> None:
        if self.volatility_1y > 0.1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasStableSharePrice',
            title='Has Stable Share Price',
            description='',
            question=f'Is their share price liquid and stable?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )

        self.descriptions = {
            'success': f'Share price is stable',
            'error': f'Shares are highly illiquid',
        }


class HasStableSharePriceOverPast3MonthsCheck(BaseCheck):
    def check(self) -> None:
        if self.volatility_3m > 0.1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasStableSharePriceOverPast3Months',
            title='Has Stable Share Price Over Past Months',
            description='',
            question=f'Over last 3 monts ss their share price liquid and stable?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Over last 3 monts share price is stable',
            'error': f'Over last 3 monts shares are highly illiquid',
        }


class HasSufficientFinancialDataCheck(BaseCheck):
    def check(self) -> None:
        if self.company_object.reports.exists():
            diff = self.get_report_diff()

            if diff.days < 180:
                self.statement['status'] = status.PASS
                self.statement['description'] = self.descriptions['success']
                self.statement['severity'] = severity.NONE
            else:
                self.statement['status'] = status.FAIL
                self.statement['description'] = self.descriptions['error']
                self.statement['severity'] = severity.MINOR
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = 'No reports'
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasSufficientFinancialData',
            title='Has Sufficient Financial Data',
            description='',
            question=f'Do they have sufficient financial data available?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Latest financial reports are less than 6 months old',
            'error': f'Latest financial reports are more than 6 months old',
        }


class IsAbleToAchieveProfitabilityCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsAbleToAchieveProfitability',
            title='Is Able To Achieve Profitability',
            description='',
            question=f'Are they forecast to achieve profitability?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )

        self.descriptions = {
            'success': f'The company is currently profitable',
            'error': f'The company is not currently profitable',
        }


class IsDividendSustainableCheck(BaseCheck):
    def check(self) -> None:
        if not self.company_dividend_is_volatile_in_10y and self.company_dividend_yield > 0.05:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsDividendSustainable',
            title='Is Dividend Sustainable',
            description='',
            question=f'Is their dividend sustainable?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )
        dividend_yield = self.get_percent_format(self.company_dividend_yield)

        self.descriptions = {
            'success': f'Dividend of {dividend_yield} is sustainable',
            'error': f'Dividend of {dividend_yield} is not sustainable',
            'no_data': f'Unstable dividend track record',
        }


class IsInAGoodFinancialPositionCheck(BaseCheck):
    def check(self) -> None:
        if self.cash_and_cash_equivalents / self.cash_expenses > 1:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsInAGoodFinancialPosition',
            title='Is In Good Financial Position',
            description='',
            question=f'Are they in a good financial position?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1001,
        )

        self.descriptions = {
            'success': f'Debt level is low and not considered a risk',
            'error': f'Has less than 1 year of cash runway',
            'no_data': f'Insufficient data',
        }


class IsProfitableOnAverageOrCurrentCheck(BaseCheck):
    def check(self) -> None:
        if self.company_earnings > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='IsProfitableOnAverageOrCurrent',
            title='Is Profitable On Average Or Current',
            description='',
            question=f'Is {self.slug.upper()} profitable on average or currently?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'Yes',
            'error': f'No',
        }


class HasNoNegativeEquityCheck(BaseCheck):
    def check(self) -> None:
        if self.equity > 0:
            self.statement['status'] = status.PASS
            self.statement['description'] = self.descriptions['success']
            self.statement['severity'] = severity.NONE
        else:
            self.statement['status'] = status.FAIL
            self.statement['description'] = self.descriptions['error']
            self.statement['severity'] = severity.MINOR

    def populate(self) -> None:
        self.statement = types.Statement(
            company=self.company_object,
            name='HasNoNegativeEquity',
            title='Negative Shareholders Equity',
            description='',
            question=f'Do they have negative shareholders equity?',
            level=level.INIT,
            area=area.RISKS,
            type=type_.RISKS,
            status=status.FAIL,
            severity=severity.NONE,
            outcome=1000,
        )

        self.descriptions = {
            'success': f'{self.slug.upper()} does not have negative shareholders equity.',
            'error': f'{self.slug.upper()} have negative shareholders equity.',
        }
