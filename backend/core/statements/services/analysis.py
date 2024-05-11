from invest.models import Company
from statements import models
from statements import types

level = types.Level
area = types.Area
type_ = types.Type
status = types.Status
severity = types.Severity


def main(companies: list[Company] = None):
    if not companies:
        companies = Company.objects.filter(is_visible=True)
    return [[
        _check_has_financial_data(c),
        _check_below_fair_value(c),
        _check_significantly_below_fair_value(c),
        _check_price_to_earnings_vs_peers(c),
        _check_price_to_earnings_vs_industry(c),
        _check_price_to_earnings_vs_fair_ratio(c),
    ] for c in companies]


def _check_has_financial_data(company_object: Company):
    slug = company_object.slug

    statement = types.Statement(
        company=company_object,
        name='HasFinancialData',
        title='Has Financial Data',
        description='',
        question=f'Does {slug.upper()} have financial data available?',
        level=level.INIT,
        area=area.RISKS,
        type=type_.RISKS,
        status=status.FAIL,
        severity=severity.NONE,
    )

    if company_object.reports.all().exists():
        statement['description'] = f'{slug.upper()} has financial data available.'
        statement['status'] = status.PASS
    else:
        statement['description'] = f'{slug.upper()} has\'t financial data available.'

    obj, is_created = models.Statement.objects.update_or_create(
        name=statement['name'],
        company=statement['company'],
        defaults=statement,
    )

    return f'{slug.upper()} on {statement["name"]} was {"created" if is_created else "updated"}'


def _check_below_fair_value(company_object: Company):
    slug = company_object.slug
    current_price = company_object.candles.order_by('-time')[0].close
    fair_price = 329.48

    statement = types.Statement(
        company=company_object,
        name='IsUndervaluedBasedOnDCF',
        title='Below Fair Value',
        description='',
        question=f'Is {slug.upper()} moderately undervalued based on cash flows?',
        level=level.GLOBAL,
        area=area.VALUE,
        type=type_.STATEMENTS,
        status=status.FAIL,
        severity=severity.NONE,
    )

    if current_price < fair_price:
        statement['status'] = status.PASS
        statement['description'] = f'{slug.upper()} ({current_price}) is trading below our estimate of fair value ({fair_price})'
    else:
        statement['description'] = f'{slug.upper()} ({current_price}) is trading above our estimate of fair value ({fair_price})'

    obj, is_created = models.Statement.objects.update_or_create(
        name=statement['name'],
        company=statement['company'],
        defaults=statement,
    )

    return f'{slug.upper()} on {statement["name"]} was {"created" if is_created else "updated"}'


def _check_significantly_below_fair_value(company_object: Company):
    slug = company_object.slug
    current_price = company_object.candles.order_by('-time')[0].close
    fair_price = 329.48

    statement = types.Statement(
        company=company_object,
        name='IsHighlyUndervaluedBasedOnDCF',
        title='Significantly Below Fair Value',
        description='',
        question=f'Is {slug.upper()} substantially undervalued based on cash flows?',
        level=level.GLOBAL,
        area=area.VALUE,
        type=type_.STATEMENTS,
        status=status.FAIL,
        severity=severity.NONE,
    )

    if (current_price - fair_price) / fair_price > 0.2:
        statement['status'] = status.PASS
        statement[
            'description'] = f'{slug.upper()} ({current_price}) is trading below fair value by more than 20%.'
    else:
        statement[
            'description'] = f'{slug.upper()} ({current_price}) is trading above our estimate of fair value.'

    obj, is_created = models.Statement.objects.update_or_create(
        name=statement['name'],
        company=statement['company'],
        defaults=statement,
    )

    return f'{slug.upper()} on {statement["name"]} was {"created" if is_created else "updated"}'


def _check_price_to_earnings_vs_peers(company_object: Company):
    slug = company_object.slug
    company_pe = 5.0
    peers_pe = 4.8
    
    statement = types.Statement(
        company=company_object,
        name='IsGoodValueComparingPriceToEarningsToPeersAverageValue',
        title='Price-To-Earnings vs Peers',
        description='',
        question=f'Is {slug.upper()} considered good value compared to its peers?',
        level=level.GLOBAL,
        area=area.VALUE,
        type=type_.STATEMENTS,
        status=status.FAIL,
        severity=severity.NONE,
    )

    if company_pe < peers_pe:
        statement['status'] = status.PASS
        statement['description'] = f'{slug.upper()} is good value based on its Price-To-Earnings Ratio ({company_pe}x) compared to the peer average ({peers_pe}x).'
    else:
        statement['description'] = f'{slug.upper()} is expensive based on its Price-To-Earnings Ratio ({company_pe}x) compared to the peer average ({peers_pe}x).'

    obj, is_created = models.Statement.objects.update_or_create(
        name=statement['name'],
        company=statement['company'],
        defaults=statement,
    )

    return f'{slug.upper()} on {statement["name"]} was {"created" if is_created else "updated"}'


def _check_price_to_earnings_vs_industry(company_object: Company):
    slug = company_object.slug
    company_pe = 5.0
    industry_pe = 4.8

    statement = types.Statement(
        company=company_object,
        name='IsGoodValueComparingPriceToEarningsToIndustry',
        title='Price-To-Earnings vs Industry',
        description='',
        question=f'Is {slug.upper()} considered good value compared to its industry?',
        level=level.GLOBAL,
        area=area.VALUE,
        type=type_.STATEMENTS,
        status=status.FAIL,
        severity=severity.NONE,
    )

    if company_pe < industry_pe:
        statement['status'] = status.PASS
        statement['description'] = f'{slug.upper()} is good value based on its Price-To-Earnings Ratio ({company_pe}x) compared to the European Banks industry average ({industry_pe}x).'
    else:
        statement['description'] = f'{slug.upper()} is expensive based on its Price-To-Earnings Ratio ({company_pe}x) compared to the US Semiconductor industry average ({industry_pe}x).'

    obj, is_created = models.Statement.objects.update_or_create(
        name=statement['name'],
        company=statement['company'],
        defaults=statement,
    )

    return f'{slug.upper()} on {statement["name"]} was {"created" if is_created else "updated"}'


def _check_price_to_earnings_vs_fair_ratio(company_object: Company):
    slug = company_object.slug
    company_pe = 5.0
    company_fair_pe = 4.8

    statement = types.Statement(
        company=company_object,
        name='IsGoodValueComparingRatioToFairRatio',
        title='Price-To-Earnings vs Fair Ratio',
        description='',
        question=f'Is {slug.upper()} considered good value compared to its fair ratio?',
        level=level.GLOBAL,
        area=area.VALUE,
        type=type_.STATEMENTS,
        status=status.FAIL,
        severity=severity.NONE,
    )

    if company_pe < company_fair_pe:
        statement['status'] = status.PASS
        statement['description'] = f'{slug.upper()} is good value based on its Price-To-Earnings Ratio ({company_pe}x) compared to the estimated Fair Price-To-Earnings Ratio ({company_fair_pe}x).'
    else:
        statement['description'] = f'{slug.upper()} is expensive based on its Price-To-Earnings Ratio ({company_pe}x) compared to the estimated Fair Price-To-Earnings Ratio ({company_fair_pe}x).'

    obj, is_created = models.Statement.objects.update_or_create(
        name=statement['name'],
        company=statement['company'],
        defaults=statement,
    )

    return f'{slug.upper()} on {statement["name"]} was {"created" if is_created else "updated"}'
