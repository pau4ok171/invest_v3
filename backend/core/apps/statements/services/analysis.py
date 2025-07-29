from apps.invest.models import Company
from apps.statements.checks.initials import (
    AreRevenueAndEarningsExpectedToGrowCheck,
    HasBeenGrowingProfitOrRevenueCheck,
    HasCapitalisationRateIncreasedSignificantlyCheck,
    HasCashFromOperationGrownSlowerThanNetIncomeCheck,
    HasDecliningGrossProfitMarginsCheck,
    HasDecliningProfitMarginsCheck,
    HasFiledWithinMonthsCheck,
    HasFiledWithinPastYearCheck,
    HasFinancialDataCheck,
    HasHighAccrualsRatioCheck,
    HasHighQualityEarningsCheck,
    HasInventoryGrownSignificantlyFasterThanSalesCheck,
    HasLargeDecreaseInUnearnedRevenueCheck,
    HasLargeIncreaseInAccountsReceivableCheck,
    HasLargeNegativeOneTimeChargesCheck,
    HasLargeOneTimeChargesCheck,
    HasLargePositiveOneTimeChargesCheck,
    HasLargePositiveOneTimeChargesAndProfitableCheck,
    HasMeaningfulMarketCapCheck,
    HasMeaningfulRevenueCheck,
    HasNegativeGrossMarginCheck,
    HasNetProfitMarginImprovedOverPastYearCheck,
    HasNoConcerningRecentEventsCheck,
    HasNoNegativeEquityCheck,
    HasNoSubstantialInsiderSellingOverPastQuarterCheck,
    HasNotDilutedOverPastYearCheck,
    HasSignificantNonOperatingRevenueCheck,
    HasStableSharePriceCheck,
    HasStableSharePriceOverPast3MonthsCheck,
    HasSufficientFinancialDataCheck,
    IsAbleToAchieveProfitabilityCheck,
    IsDividendAttractiveCheck,
    IsDividendSustainableCheck,
    IsGoodRelativeValueCheck,
    IsGoodValueCheck,
    IsGoodValueComparedToIndustryCheck,
    IsGoodValueComparedToPeersCheck,
    IsGrowingProfitOrRevenueCheck,
    IsInAGoodFinancialPositionCheck,
    IsProfitableOnAverageOrCurrentCheck,
    IsTradingBelowAnalystPriceTargetsCheck,
    IsTradingBelowFairRatioCheck,
)
from apps.statements.types import Fields
from apps.statements.checks.value import (
    BelowFairValueCheck,
    SignificantlyBelowFairValueCheck,
    PriceToEarningsVsPeersCheck,
    PriceToEarningsVsIndustryCheck,
    PriceToEarningsVsFairRatioCheck,
    AnalystForecastCheck,
    ReturnVsMarketCheck,
    ReturnVsIndustryCheck,
)
from apps.statements.checks.future import (
    EarningsVsSavingRateCheck,
    EarningsVsMarketCheck,
    HighGrowthEarningsCheck,
    RevenueVsMarketCheck,
    HighGrowthRevenueCheck,
    FutureROECheck,
)
from apps.statements.checks.past import (
    QualityEarningsCheck,
    GrowingProfitMarginCheck,
    EarningsTrendCheck,
    AcceleratingGrowthCheck,
    EarningsVsIndustryCheck,
    HighROECheck,
    StableSharePriceCheck,
    VolatilityOverTimeCheck,
)
from apps.statements.checks.health import (
    ShortTermLiabilitiesCheck,
    LongTermLiabilitiesCheck,
    DebtLevelCheck,
    ReducingDebtCheck,
    DebtCoverageCheck,
    InterestCoverageCheck,
)
from apps.statements.checks.dividend import (
    SignificantDividendCheck,
    HighDividendCheck,
    StableDividendCheck,
    GrowingDividendCheck,
    EarningsCoverageCheck,
    CashFlowCoverageCheck,
)


def main(companies: list[Company] = None):
    if not companies:
        companies = Company.objects.filter(is_visible=True)

    objects = []

    for company in companies:
        if not company.candles.order_by('-time').exists():
            continue

        fields = get_fields(company)
        
        checks = [
            # INIT
            AreRevenueAndEarningsExpectedToGrowCheck(fields).to_dict(),
            HasBeenGrowingProfitOrRevenueCheck(fields).to_dict(),
            HasCapitalisationRateIncreasedSignificantlyCheck(fields).to_dict(),
            HasCashFromOperationGrownSlowerThanNetIncomeCheck(fields).to_dict(),
            HasDecliningGrossProfitMarginsCheck(fields).to_dict(),
            HasDecliningProfitMarginsCheck(fields).to_dict(),
            HasFiledWithinMonthsCheck(fields).to_dict(),
            HasFiledWithinPastYearCheck(fields).to_dict(),
            HasFinancialDataCheck(fields).to_dict(),
            HasHighAccrualsRatioCheck(fields).to_dict(),
            HasHighQualityEarningsCheck(fields).to_dict(),
            HasInventoryGrownSignificantlyFasterThanSalesCheck(fields).to_dict(),
            HasLargeDecreaseInUnearnedRevenueCheck(fields).to_dict(),
            HasLargeIncreaseInAccountsReceivableCheck(fields).to_dict(),
            HasLargeNegativeOneTimeChargesCheck(fields).to_dict(),
            HasLargeOneTimeChargesCheck(fields).to_dict(),
            HasLargePositiveOneTimeChargesCheck(fields).to_dict(),
            HasLargePositiveOneTimeChargesAndProfitableCheck(fields).to_dict(),
            HasMeaningfulMarketCapCheck(fields).to_dict(),
            HasMeaningfulRevenueCheck(fields).to_dict(),
            HasNegativeGrossMarginCheck(fields).to_dict(),
            HasNetProfitMarginImprovedOverPastYearCheck(fields).to_dict(),
            HasNoConcerningRecentEventsCheck(fields).to_dict(),
            HasNoNegativeEquityCheck(fields).to_dict(),
            HasNoSubstantialInsiderSellingOverPastQuarterCheck(fields).to_dict(),
            HasNotDilutedOverPastYearCheck(fields).to_dict(),
            HasSignificantNonOperatingRevenueCheck(fields).to_dict(),
            HasStableSharePriceCheck(fields).to_dict(),
            HasStableSharePriceOverPast3MonthsCheck(fields).to_dict(),
            HasSufficientFinancialDataCheck(fields).to_dict(),
            IsAbleToAchieveProfitabilityCheck(fields).to_dict(),
            IsDividendAttractiveCheck(fields).to_dict(),
            IsDividendSustainableCheck(fields).to_dict(),
            IsGoodRelativeValueCheck(fields).to_dict(),
            IsGoodValueCheck(fields).to_dict(),
            IsGoodValueComparedToIndustryCheck(fields).to_dict(),
            IsGoodValueComparedToPeersCheck(fields).to_dict(),
            IsGrowingProfitOrRevenueCheck(fields).to_dict(),
            IsInAGoodFinancialPositionCheck(fields).to_dict(),
            IsProfitableOnAverageOrCurrentCheck(fields).to_dict(),
            IsTradingBelowAnalystPriceTargetsCheck(fields).to_dict(),
            IsTradingBelowFairRatioCheck(fields).to_dict(),
            # VALUE
            BelowFairValueCheck(fields).to_dict(),
            SignificantlyBelowFairValueCheck(fields).to_dict(),
            PriceToEarningsVsPeersCheck(fields).to_dict(),
            PriceToEarningsVsIndustryCheck(fields).to_dict(),
            PriceToEarningsVsFairRatioCheck(fields).to_dict(),
            AnalystForecastCheck(fields).to_dict(),
            ReturnVsMarketCheck(fields).to_dict(),
            ReturnVsIndustryCheck(fields).to_dict(),
            # FUTURE
            EarningsVsSavingRateCheck(fields).to_dict(),
            EarningsVsMarketCheck(fields).to_dict(),
            HighGrowthEarningsCheck(fields).to_dict(),
            RevenueVsMarketCheck(fields).to_dict(),
            HighGrowthRevenueCheck(fields).to_dict(),
            FutureROECheck(fields).to_dict(),
            # PAST
            QualityEarningsCheck(fields).to_dict(),
            GrowingProfitMarginCheck(fields).to_dict(),
            EarningsTrendCheck(fields).to_dict(),
            AcceleratingGrowthCheck(fields).to_dict(),
            EarningsVsIndustryCheck(fields).to_dict(),
            HighROECheck(fields).to_dict(),
            StableSharePriceCheck(fields).to_dict(),
            VolatilityOverTimeCheck(fields).to_dict(),
            # HEALTH
            ShortTermLiabilitiesCheck(fields).to_dict(),
            LongTermLiabilitiesCheck(fields).to_dict(),
            DebtLevelCheck(fields).to_dict(),
            ReducingDebtCheck(fields).to_dict(),
            DebtCoverageCheck(fields).to_dict(),
            InterestCoverageCheck(fields).to_dict(),
            # DIVIDEND
            SignificantDividendCheck(fields).to_dict(),
            HighDividendCheck(fields).to_dict(),
            StableDividendCheck(fields).to_dict(),
            GrowingDividendCheck(fields).to_dict(),
            EarningsCoverageCheck(fields).to_dict(),
            CashFlowCoverageCheck(fields).to_dict(),
        ]

        objects.append(checks)

    return objects


def get_fields(company_object):
    last_candle = company_object.candles.order_by('-time').first()

    return Fields(
        # Common
        company_object=company_object,
        slug=company_object.slug,
        currency='₽',
        market_country_adjectif='russian',
        sector_company_name='banks',
        # Value
        company_current_price=last_candle.close if last_candle else 0,
        average_price_target_1y=400,
        company_fair_price=329.48,
        company_pe=5.0,
        peers_pe=4.8,
        industry_pe=4.8,
        company_fair_pe=4.8,
        return_1y=0.33,
        market_return_1y=0.282,
        sector_market_return_1y=0.299,
        # Future
        company_forecast_earnings_growth=0.082,
        country_saving_rate=0.075,
        market_forecast_earnings_growth=0.092,
        company_forecast_revenue_growth=0.0125,
        market_forecast_revenue_growth=0.033,
        company_future_roe_3y=0.0199,
        # Past
        company_earnings=1_158_600_000_000,
        company_profit_margins=0.476,
        past_profit_margins=0.419,
        company_earnings_growth_5y=0.101,
        company_earnings_growth=0.524,
        industry_earnings_growth=0.146,
        company_roe=0.209,
        volatility_3m=0.017,
        volatility_1y=0.29,
        volatility_1y_past_year=0.17,
        sector_market_volatility_3m=0.032,
        # Health
        company_short_term_assets=6_271_400_000_000,
        company_short_term_liabilities=31_154_700_000_000,
        company_long_term_liabilities=4_366_300_000_000,
        company_net_debt_to_equity_ratio=0.027,
        company_debt=9_700_000_000,
        company_debt_to_equity_ratio=0.903,
        company_debt_to_equity_ratio_5Y_ago=0.99,
        company_operating_cash_flow=-100_000_000,
        company_interest_rate=0.09,
        company_ebit=100_000_000,
        # Dividend
        company_dividend_yield=0.1403,
        market_dividend_yield_p25=0.0443,
        market_dividend_yield_p75=0.1315,
        company_dividend_is_volatile_in_10y=True,
        company_dividend_amount=539_673_700_000,
        company_dividend_amount_10y_ago=55_678_456_360,
        company_payout_ratio=0.347,
        company_cash_payout_ratio=0,
        # Risks
        earnings_growth_per_year_forecast_3y=0.082,
        capitalisation_rate=0.07,
        capitalisation_rate_1y=0.05,
        operating_cash_flow_growth=0.6,
        gross_profit_margin=0.97,
        gross_profit_margin_1y=0.98,
        sloan_ratio=0.15,  # =(Net Income-CFO(Cash Flow from Operations)-CFI(Cash Flow from Investments))/Total Assets
        inventory_growth=0.20,
        sales_growth=0.25,
        unearned_revenue_growth=0.25,
        accounts_receivable_growth=0.25,
        one_off_charges=5_000_000,
        market_cap_usd=42_000_000_000,
        market_cap=4_000_000_000_000,
        revenue=3_000_000_000_000,
        events_was_occurred=True,
        substantial_insider_selling_was_occurred=True,
        has_diluted_over_past_year=True,
        non_operating_revenue=100_000_000,
        operating_revenue=1_500_000_000_000,
        cash_and_cash_equivalents=100_000_000,
        cash_expenses=50_000_000,
        equity=5_000_000_000,
    )
