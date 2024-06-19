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
