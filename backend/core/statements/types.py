from enum import Enum
from typing import TypedDict
from invest.models import Company


class ExtendedEnum(Enum):
    @classmethod
    def as_dict(cls):
        return dict(map(lambda item: (item.name, item.value.capitalize()), cls))

    def __str__(self):
        return self.name


class Level(ExtendedEnum):
    INIT = 'INIT'
    GLOBAL = 'GLOBAL'
    SECTOR = 'SECTOR'


class Area(ExtendedEnum):
    RISKS = 'RISKS'
    REWARDS = 'REWARDS'
    OVERVIEW = 'OVERVIEW'
    VALUE = 'VALUE'
    FUTURE = 'FUTURE'
    PAST = 'PAST'
    HEALTH = 'HEALTH'
    DIVIDENDS = 'DIVIDENDS'
    MANAGEMENT = 'MANAGEMENT'
    OWNERSHIP = 'OWNERSHIP'
    MISC = 'MISC'


class Type(ExtendedEnum):
    RISKS = 'RISKS'
    STATEMENTS = 'STATEMENTS'
    REWARDS = 'REWARDS'


class Status(ExtendedEnum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    NODATA = 'NODATA'


class Severity(ExtendedEnum):
    NONE = 'NONE'
    MINOR = 'MINOR'
    MAJOR = 'MAJOR'


class Statement(TypedDict):
    company: Company
    name: str
    title: str
    description: str
    question: str
    level: Level
    area: Area
    type: Type
    status: Status
    severity: Severity


class Fields(TypedDict):
    company_object: Company
    slug: str
    current_price: float
    fair_price: float
    company_pe: float
    peers_pe: float
    industry_pe: float
    fair_pe: float
