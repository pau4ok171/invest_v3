from invest.models import Company
from statements.checks.initials import HasFinancialDataCheck
from statements.types import Fields
from statements.checks.value import (
    BelowFairValueCheck,
    SignificantlyBelowFairValueCheck,
    PriceToEarningsVsPeersCheck,
    PriceToEarningsVsIndustryCheck,
    PriceToEarningsVsFairRatioCheck,
)


def main(companies: list[Company] = None):
    if not companies:
        companies = Company.objects.filter(is_visible=True)

    objects = []

    for company in companies:
        fields = get_fields(company)

        objects.append([
            HasFinancialDataCheck(fields),
            BelowFairValueCheck(fields),
            SignificantlyBelowFairValueCheck(fields),
            PriceToEarningsVsPeersCheck(fields),
            PriceToEarningsVsIndustryCheck(fields),
            PriceToEarningsVsFairRatioCheck(fields),
        ])

    return objects


def get_fields(company_object):
    return Fields(
        company_object=company_object,
        slug=company_object.slug,
        current_price=company_object.candles.order_by('-time')[0].close,
        fair_price=329.48,
        company_pe=5.0,
        peers_pe=4.8,
        industry_pe=4.8,
        fair_pe=4.8,
    )
