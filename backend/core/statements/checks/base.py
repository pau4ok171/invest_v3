from invest.models import Company
from statements import models
from statements.types import Statement


class BaseCheck:
    def __init__(self, fields: dict):
        self.statement: Statement | None = None
        self.company_object: Company | None = None
        self.slug: str | None = None
        self.description: str | None = None

        self.current_price: float | None = None
        self.fair_price: float | None = None
        self.company_pe: float | None = None
        self.peers_pe: float | None = None
        self.industry_pe: float | None = None
        self.fair_pe: float | None = None

        for k, v in fields.items():
            setattr(self, k, v)

        self._process()

    def _process(self):
        self.populate()
        self.check()
        self._create_or_update()
        return f'{self.slug.upper()} on {self.statement["name"]} was {"created" if self.is_created else "updated"}'

    def _create_or_update(self):
        _, self.is_created = models.Statement.objects.update_or_create(
            name=self.statement['name'],
            company=self.statement['company'],
            defaults=self.statement,
        )

    def _validate(self):
        pass

    def check(self):
        pass

    def populate(self):
        pass
