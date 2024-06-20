from invest.models import Company
from statements.checks.initials import HasFinancialDataCheck
from statements.types import Fields
from statements.checks.value import (
    BelowFairValueCheck,
    SignificantlyBelowFairValueCheck,
    PriceToEarningsVsPeersCheck,
    PriceToEarningsVsIndustryCheck,
    PriceToEarningsVsFairRatioCheck,
    ReturnVsMarketCheck,
    ReturnVsIndustryCheck,
)
from statements.checks.future import (
    EarningsVsSavingRateCheck,
    EarningsVsMarketCheck,
    HighGrowthEarningsCheck,
    RevenueVsMarketCheck,
    HighGrowthRevenueCheck,
    FutureROECheck,
)
from statements.checks.past import (
    QualityEarningsCheck,
    GrowingProfitMarginCheck,
    EarningsTrendCheck,
    AcceleratingGrowthCheck,
    EarningsVsIndustryCheck,
    HighROECheck,
    StableSharePriceCheck,
    VolatilityOverTimeCheck,
)
from statements.checks.health import (
    ShortTermLiabilitiesCheck,
    LongTermLiabilitiesCheck,
    DebtLevelCheck,
    ReducingDebtCheck,
    DebtCoverageCheck,
    InterestCoverageCheck,
)
from statements.checks.dividend import (
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
        fields = get_fields(company)

        objects.append([
            # INIT
            HasFinancialDataCheck(fields),
            # VALUE
            BelowFairValueCheck(fields),
            SignificantlyBelowFairValueCheck(fields),
            PriceToEarningsVsPeersCheck(fields),
            PriceToEarningsVsIndustryCheck(fields),
            PriceToEarningsVsFairRatioCheck(fields),
            ReturnVsMarketCheck(fields),
            ReturnVsIndustryCheck(fields),
            # FUTURE
            EarningsVsSavingRateCheck(fields),
            EarningsVsMarketCheck(fields),
            HighGrowthEarningsCheck(fields),
            RevenueVsMarketCheck(fields),
            HighGrowthRevenueCheck(fields),
            FutureROECheck(fields),
            # PAST
            QualityEarningsCheck(fields),
            GrowingProfitMarginCheck(fields),
            EarningsTrendCheck(fields),
            AcceleratingGrowthCheck(fields),
            EarningsVsIndustryCheck(fields),
            HighROECheck(fields),
            StableSharePriceCheck(fields),
            VolatilityOverTimeCheck(fields),
            # HEALTH
            ShortTermLiabilitiesCheck(fields),
            LongTermLiabilitiesCheck(fields),
            DebtLevelCheck(fields),
            ReducingDebtCheck(fields),
            DebtCoverageCheck(fields),
            InterestCoverageCheck(fields),
            # DIVIDEND
            SignificantDividendCheck(fields),
            HighDividendCheck(fields),
            StableDividendCheck(fields),
            GrowingDividendCheck(fields),
            EarningsCoverageCheck(fields),
            CashFlowCoverageCheck(fields),
        ])

    return objects


def get_fields(company_object):
    return Fields(
        # Common
        company_object=company_object,
        slug=company_object.slug,
        currency='₽',
        market_country_adjectif='russian',
        sector_company_name='banks',
        # Value
        company_current_price=company_object.candles.order_by('-time')[0].close,
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
    )
