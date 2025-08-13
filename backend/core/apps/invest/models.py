from enum import Enum

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

from parler.models import TranslatableModel, TranslatedFields

from .model_choices import QUARTERS, REPORT_FORMS, SCALES

URL_PREFIX = settings.URL_PREFIX


class ReportPeriodType(Enum):
    ANNUAL = 'annual'
    QUARTERLY = 'quarterly'


def logo_directory_path(instance, filename):
    return f'companies/logos/small/{instance.ticker.upper()}_{filename}'


class SectorGroup(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(max_length=255)
    )
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    class Meta:
        ordering = ['translations__title']
        indexes = [
            models.Index(fields=['slug'])
        ]


class Sector(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        description=models.TextField(null=True, blank=True)
    )
    slug = models.SlugField(max_length=255, unique=True)
    main_header = models.ImageField(
        upload_to='companies/header',
        default='companies/header/default.png',
        blank=True
    )
    sector_group = models.ForeignKey(SectorGroup, on_delete=models.PROTECT, related_name='sectors')

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    class Meta:
        ordering = ['translations__title']
        indexes = [
            models.Index(fields=['slug'])
        ]


class Company(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        short_title=models.CharField(max_length=255, null=True, blank=True),
        short_title_genitive=models.CharField(max_length=255, null=True, blank=True),
        description=models.TextField(blank=True, default='No description yet'),
        short_description=models.TextField(blank=True, default='No description yet'),
        city=models.CharField(max_length=255, null=True, blank=True),
    )
    ticker = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=25, unique=True)
    uid = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    market = models.ForeignKey('Market', on_delete=models.PROTECT)
    sector = models.ForeignKey('Sector', on_delete=models.PROTECT)
    industry = models.ForeignKey('Industry', on_delete=models.PROTECT)
    sector_group = models.ForeignKey('SectorGroup', on_delete=models.PROTECT, related_name='companies')
    created = models.DateTimeField(null=False, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    is_visible = models.BooleanField(default=False, help_text='If company is visible publicly')
    logo = models.ImageField(
        upload_to=logo_directory_path,
        blank=True,
        default='companies/logos/default.png'
    )
    is_fund = models.BooleanField(default=False, help_text='If company is invest fund')
    website = models.URLField(null=True, blank=True)
    year_founded = models.PositiveSmallIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='company_created_by',
        null=False,
        blank=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='company_updated_by',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    def get_absolute_url(self):
        return f'/markets/{self.slug}/'

    def get_logo(self):
        if self.logo:
            return URL_PREFIX + self.logo.url
        return ''

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_visible']),
        ]
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class CompanyPerformance(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='performance')
    return_7d = models.FloatField(null=True, blank=True)
    return_30d = models.FloatField(null=True, blank=True)
    return_90d = models.FloatField(null=True, blank=True)
    return_1y = models.FloatField(null=True, blank=True)
    return_3y = models.FloatField(null=True, blank=True)
    return_5y = models.FloatField(null=True, blank=True)
    average_weekly_movement = models.FloatField(null=True, blank=True)
    last_reported_earnings = models.DateField(null=True, blank=True)
    next_earnings = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Company Performance'
        verbose_name_plural = 'Companies\' Performance'


class Industry(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
    )
    slug = models.SlugField(max_length=255, unique=True)
    sector = models.ForeignKey('Sector', on_delete=models.PROTECT)

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    class Meta:
        ordering = ['translations__title']
        indexes = [
            models.Index(fields=['slug'])
        ]
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'


class Country(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        name_genitive=models.CharField(max_length=255),

    )
    iso_code = models.CharField(max_length=3)
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, related_name='countries')

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    class Meta:
        ordering = ['translations__name']

        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Currency(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
    )
    iso_code = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Analyst(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=255),
        description=models.TextField(null=True, blank=True),
    )
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True)


class Market(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT, related_name='market', null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['slug'])
        ]


class MarketPerformance(models.Model):
    market = models.OneToOneField(Market, on_delete=models.CASCADE, related_name='performance')
    return_7d = models.FloatField(null=True, blank=True)
    return_30d = models.FloatField(null=True, blank=True)
    return_90d = models.FloatField(null=True, blank=True)
    return_1y = models.FloatField(null=True, blank=True)
    return_3y = models.FloatField(null=True, blank=True)
    return_5y = models.FloatField(null=True, blank=True)
    average_weekly_mouvement = models.FloatField(null=True, blank=True)
    # percents
    volatility_0p = models.FloatField(null=True, blank=True)
    volatility_10p = models.FloatField(null=True, blank=True)
    volatility_25p = models.FloatField(null=True, blank=True)
    volatility_50p = models.FloatField(null=True, blank=True)
    volatility_75p = models.FloatField(null=True, blank=True)
    volatility_90p = models.FloatField(null=True, blank=True)
    volatility_100p = models.FloatField(null=True, blank=True)


class SectorMarket(models.Model):
    sector = models.ForeignKey('Sector', on_delete=models.CASCADE)
    market = models.ForeignKey('Market', on_delete=models.CASCADE)
    return_7d = models.FloatField(null=True, blank=True)
    return_30d = models.FloatField(null=True, blank=True)
    return_90d = models.FloatField(null=True, blank=True)
    return_1y = models.FloatField(null=True, blank=True)
    return_3y = models.FloatField(null=True, blank=True)
    return_5y = models.FloatField(null=True, blank=True)
    average_weekly_mouvement = models.FloatField(null=True, blank=True)
    # percents
    volatility_0p = models.FloatField(null=True, blank=True)
    volatility_10p = models.FloatField(null=True, blank=True)
    volatility_25p = models.FloatField(null=True, blank=True)
    volatility_50p = models.FloatField(null=True, blank=True)
    volatility_75p = models.FloatField(null=True, blank=True)
    volatility_90p = models.FloatField(null=True, blank=True)
    volatility_100p = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.market.title} - {self.sector.__str__()}'


class ReportMetadata(models.Model):
    company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name='report')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    verified = models.DateTimeField(blank=True, null=True)
    is_analysed = models.BooleanField(default=False)
    is_automatically_collected = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    # Summary
    year = models.IntegerField()
    quarter = models.PositiveSmallIntegerField(choices=QUARTERS)
    report_period_type = models.CharField(choices=[(tag.value, tag.name) for tag in ReportPeriodType], max_length=10)
    report_form = models.CharField(choices=REPORT_FORMS, max_length=12)
    scale = models.CharField(choices=SCALES, max_length=12)
    scale_unit = models.IntegerField(default=1)
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    # Additional Info
    share_outstanding_eop = models.DecimalField(max_digits=15, decimal_places=2, default=0)  # end of period
    total_employees_figure = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.company} - {self.quarter} - {self.year}'

    class Meta:
        ordering = ['-year', '-quarter']
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'year', 'quarter', 'report_period_type'],
                name='unique_company_report',
            )
        ]


class BalanceSheet(models.Model):
    report = models.OneToOneField(ReportMetadata, on_delete=models.CASCADE, related_name='balance_sheet')
    # Balance Sheet
    accounts_payable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    accounts_payable_and_accrued_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    accounts_payable_and_accrued_expense_for_financial_companies = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    accounts_receivable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    accumulated_depreciation = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    accumulated_other_comprehensive_income_or_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    additional_paid_in_capital = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    allowance_for_loans_and_lease_losses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    buildings_and_improvements = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_and_cash_equivalents = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balance_sheet_cash_and_cash_equivalents = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_and_cash_equivalents_and_marketable_securities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    common_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    construction_in_progress = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_accrued_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_deferred_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_deferred_taxes_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    deferred_policy_acquisition_costs = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    deferred_tax_and_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    equity_investments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fixed_maturity_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    future_policy_benefits = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    goodwill = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gross_loan = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gross_property_and_plant_and_equipment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    intangible_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    inventories_and_finished_good = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    inventories_and_inventories_adjustments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    inventories_and_other = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    inventories_and_raw_materials_and_components = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    inventories_and_work_in_process = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    investments_and_advanced = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    land_and_improvements = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    loans_receivable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    long_term_capital_lease_obligation = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    long_term_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    long_term_debt_and_capital_lease_obligation = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    machinery_and_furniture_and_equipment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    marketable_securities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    minority_interest = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    money_market_investments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_loan = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    non_current_deferred_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    notes_receivable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_assets_for_banks = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_assets_for_insurance_companies = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_current_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_current_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_current_payables = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_current_receivables = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_gross_ppe = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_liabilities_for_banks = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_liabilities_for_insurance_companies = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_long_term_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_long_term_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_stockholders_equity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pension_and_retirement_benefit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    policyholder_funds = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    preferred_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    property_and_plant_and_equipment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    retained_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    securities_and_investments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    short_term_capital_lease_obligation = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    short_term_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    short_term_debt_and_capital_lease_obligation = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    short_term_investments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_current_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_current_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_deposits = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_equity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_inventories = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_long_term_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_long_term_liabilities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_receivables = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_stockholders_equity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_tax_payable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    treasury_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unearned_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unearned_premiums = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    unpaid_loss_and_loss_reserve = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class IncomeStatement(models.Model):
    report = models.OneToOneField(ReportMetadata, on_delete=models.CASCADE, related_name='income_statement')
    # Income Statement
    cost_of_goods_sold = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit_losses_provision = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    depreciation_and_depletion_and_amortization = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ebit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ebitda = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    eps_basic = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    eps_diluted = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fees_and_other_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    general_and_administrative_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gross_profit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interest_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interest_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_income_continuing_operations = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_income_discontinued_operations = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_income_including_noncontrolling_interests = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_interest_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_interest_income_for_banks = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_investment_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_policyholder_benefits_or_claims = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    non_interest_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    non_operation_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    operating_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_income_minority_interest = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_net_income_or_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_noninterest_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_operating_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    policy_acquisition_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    pretax_income = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    preferred_dividends = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    research_and_development = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    selling_and_marketing_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    selling_and_general_and_administrative_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    shares_outstanding_basic_average = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    shares_outstanding_diluted_average = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    special_charges = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_provision = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_noninterest_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_operating_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_premiums_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class CashflowStatement(models.Model):
    report = models.OneToOneField(ReportMetadata, on_delete=models.CASCADE, related_name='cashflow_statement')
    # Cashflow Statement
    all_taxes_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    asset_impairment_charge = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    beginning_cash_position = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    capital_expenditure = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_flow_for_dividends = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_flow_for_lease_financing = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_flow_from_discontinued_operations = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_flow_from_financing = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_flow_from_investing = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_flow_from_operations = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_flow_from_others = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_from_discontinued_investing_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_from_discontinued_operating_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_from_other_investing_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_paid_for_insurance_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_payments = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_payments_for_deposits_by_banks_and_customers = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_payments_for_loans = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_receipts_from_deposits_by_banks_and_customers = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_receipts_from_fees_and_commissions = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_receipts_from_loans = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_receipts_from_operating_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_receipts_from_securities_related_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_receipts_from_tax_refunds = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    cash_receipts_from_insurance_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    change_in_inventory = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    change_in_other_working_capital = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    change_in_payables_and_accrued_expense = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    change_in_prepaid_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    change_in_receivables = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    change_in_working_capital = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    deferred_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    depreciation_and_depletion_and_amortization_cash_flow = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dividends_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    dividends_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    effect_of_exchange_rate_changes = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ending_cash_position = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    ffo = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    free_cash_flow = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interest_and_commission_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interest_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interest_received = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    issuance_of_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    issuance_of_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_change_in_cash = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_income_from_continuing_operations = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_intangibles_purchase_and_sale = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_issuance_of_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_issuance_of_preferred_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_cash_payments_from_operating_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_cash_receipts_from_operating_activities = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    other_financing = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payments_of_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payments_on_behalf_of_employees = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    payments_to_suppliers_for_goods_and_services = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_of_business = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_of_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    purchase_of_property_and_plant_and_equipment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    receipts_from_customers = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    receipts_from_government_grants = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    repurchase_of_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sale_of_business = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sale_of_investment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    sale_of_property_and_plant_and_equipment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    stock_based_compensation = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    taxes_refund_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)


class CandlePerDay(models.Model):
    company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name='candle')
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    time = models.DateTimeField()
    is_complete = models.BooleanField()

    class Meta:
        ordering = ['time']
        unique_together = [['company', 'time']]

        verbose_name = 'Candle Per Day'
        verbose_name_plural = 'Candles Per Day'


class AnalystIdea(models.Model):
    analyst = models.ForeignKey('Analyst', on_delete=models.PROTECT)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name='analyst_idea')
    price_target = models.FloatField()
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    date_target = models.DateTimeField()
    idea_created = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.analyst}:{self.company}'


class Dividend(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='dividend')
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    scale = models.CharField(choices=SCALES, max_length=12)
    scale_unit = models.IntegerField(default=1)
    dividend_yield = models.FloatField()
    dividend_amount = models.FloatField()
    declared_date = models.DateField()
    ex_dividend_date = models.DateField()
    pay_date = models.DateField()
