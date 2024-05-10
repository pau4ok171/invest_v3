from invest.models import Company
from statements import models
from statements import types


def main():
    companies = Company.objects.filter(is_visible=True)
    return [check_has_financial_data(c) for c in companies]


def check_has_financial_data(company_object):
    slug = company_object.slug
    statement = types.Statement(
        company=company_object,
        name='HasFinancialData',
        title='Has Financial Data',
        description=f'{slug.upper()} has\'t financial data available.',
        question=f'Does {slug.upper()} have financial data available?',
        level=types.Level.INIT,
        area=types.Area.RISKS,
        type=types.Type.RISKS,
        status=types.Status.FAIL,
        severity=types.Severity.NONE,
    )

    if company_object.reports.all().exists():
        statement['description'] = f'{slug.upper()} has financial data available.'
        statement['status'] = types.Status.PASS

    obj, is_created = models.Statement.objects.update_or_create(
        name=statement['name'],
        company=statement['company'],
        defaults=statement,
    )

    return f'{slug.upper()} was {"created" if is_created else "updated"}'
