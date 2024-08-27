import os

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from .model_choices import QUARTERS, REPORT_TYPES, REPORT_FORMS, SCALES
from notes.models import Note

URL_PREFIX = settings.URL_PREFIX


def logo_directory_path(instance, filename):
    return f'companies/logos/small/{instance.ticker.upper()}_{filename}'


class Company(models.Model):
    ticker = models.CharField(max_length=12, unique=True)
    slug = models.SlugField(max_length=25, unique=True)
    uid = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    short_title = models.CharField(max_length=255, null=True, blank=True)
    short_title_genitive = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, default='No description yet')
    short_description = models.TextField(blank=True, default='No description yet')
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT)
    market = models.ForeignKey('Market', on_delete=models.PROTECT)
    sector = models.ForeignKey('Sector', on_delete=models.PROTECT)
    industry = models.ForeignKey('Industry', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=False, help_text='If company is visible publicly')
    logo = models.ImageField(
        upload_to=logo_directory_path,
        blank=True,
        default=os.path.join(settings.MEDIA_ROOT, 'companies/logos/default.png')
    )
    is_fund = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    year_founded = models.IntegerField(null=True, blank=True)
    users_watchlist = models.ManyToManyField(
        User,
        related_name='companies_watchlisted',
        blank=True
    )
    notes = models.ManyToManyField(User, through=Note)
    last_reported_earnings = models.DateField(null=True, blank=True)
    next_earnings = models.DateField(null=True, blank=True)
    return_7d = models.FloatField(null=True, blank=True)
    return_30d = models.FloatField(null=True, blank=True)
    return_90d = models.FloatField(null=True, blank=True)
    return_1y = models.FloatField(null=True, blank=True)
    return_3y = models.FloatField(null=True, blank=True)
    return_5y = models.FloatField(null=True, blank=True)
    average_weekly_mouvement = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='company_created_by')
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='company_updated_by',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/markets/{self.slug}/'

    def get_logo(self):
        if self.logo:
            return URL_PREFIX + self.logo.url
        return ''

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['slug'])
        ]
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Market(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT, related_name='markets', null=True)
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
        return self.title

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['slug'])
        ]


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
        return f'{self.market.title} - {self.sector.title}'


class Sector(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    main_header = models.ImageField(
        upload_to='companies/header',
        default='companies/header/default.png',
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['slug'])
        ]


class Industry(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    sector = models.ForeignKey('Sector', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['slug'])
        ]
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'


class Report(models.Model):
    company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name='reports')
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
    report_type = models.CharField(choices=REPORT_TYPES, max_length=12)
    report_form = models.CharField(choices=REPORT_FORMS, max_length=12)
    scale = models.CharField(choices=SCALES, max_length=12)
    scale_unit = models.IntegerField(default=1)
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    # Balance Sheet
    accounts_payable = models.FloatField(default=0)
    accounts_payable_and_accrued_expense = models.FloatField(default=0)
    accounts_payable_and_accrued_expense_for_financial_companies = models.FloatField(default=0)
    accounts_receivable = models.FloatField(default=0)
    accumulated_depreciation = models.FloatField(default=0)
    accumulated_other_comprehensive_income_or_loss = models.FloatField(default=0)
    additional_paid_in_capital = models.FloatField(default=0)
    allowance_for_loans_and_lease_losses = models.FloatField(default=0)
    buildings_and_improvements = models.FloatField(default=0)
    cash_and_cash_equivalents = models.FloatField(default=0)
    balance_sheet_cash_and_cash_equivalents = models.FloatField(default=0)
    cash_and_cash_equivalents_and_marketable_securities = models.FloatField(default=0)
    common_stock = models.FloatField(default=0)
    construction_in_progress = models.FloatField(default=0)
    current_accrued_expense = models.FloatField(default=0)
    current_deferred_revenue = models.FloatField(default=0)
    current_deferred_taxes_liabilities = models.FloatField(default=0)
    deferred_policy_acquisition_costs = models.FloatField(default=0)
    deferred_tax_and_revenue = models.FloatField(default=0)
    equity_investments = models.FloatField(default=0)
    fixed_maturity_investment = models.FloatField(default=0)
    future_policy_benefits = models.FloatField(default=0)
    goodwill = models.FloatField(default=0)
    gross_loan = models.FloatField(default=0)
    gross_property_and_plant_and_equipment = models.FloatField(default=0)
    intangible_assets = models.FloatField(default=0)
    inventories_and_finished_good = models.FloatField(default=0)
    inventories_and_inventories_adjustments = models.FloatField(default=0)
    inventories_and_other = models.FloatField(default=0)
    inventories_and_raw_materials_and_components = models.FloatField(default=0)
    inventories_and_work_in_process = models.FloatField(default=0)
    investments_and_advanced = models.FloatField(default=0)
    land_and_improvements = models.FloatField(default=0)
    loans_receivable = models.FloatField(default=0)
    long_term_capital_lease_obligation = models.FloatField(default=0)
    long_term_debt = models.FloatField(default=0)
    long_term_debt_and_capital_lease_obligation = models.FloatField(default=0)
    machinery_and_furniture_and_equipment = models.FloatField(default=0)
    marketable_securities = models.FloatField(default=0)
    minority_interest = models.FloatField(default=0)
    money_market_investments = models.FloatField(default=0)
    net_loan = models.FloatField(default=0)
    non_current_deferred_liabilities = models.FloatField(default=0)
    notes_receivable = models.FloatField(default=0)
    other_assets_for_banks = models.FloatField(default=0)
    other_assets_for_insurance_companies = models.FloatField(default=0)
    other_current_assets = models.FloatField(default=0)
    other_current_liabilities = models.FloatField(default=0)
    other_current_payables = models.FloatField(default=0)
    other_current_receivables = models.FloatField(default=0)
    other_gross_ppe = models.FloatField(default=0)
    other_liabilities_for_banks = models.FloatField(default=0)
    other_liabilities_for_insurance_companies = models.FloatField(default=0)
    other_long_term_assets = models.FloatField(default=0)
    other_long_term_liabilities = models.FloatField(default=0)
    other_stockholders_equity = models.FloatField(default=0)
    pension_and_retirement_benefit = models.FloatField(default=0)
    policyholder_funds = models.FloatField(default=0)
    preferred_stock = models.FloatField(default=0)
    property_and_plant_and_equipment = models.FloatField(default=0)
    retained_earnings = models.FloatField(default=0)
    securities_and_investments = models.FloatField(default=0)
    share_outstanding_eop = models.FloatField(default=0)  # end of period
    short_term_capital_lease_obligation = models.FloatField(default=0)
    short_term_debt = models.FloatField(default=0)
    short_term_debt_and_capital_lease_obligation = models.FloatField(default=0)
    short_term_investments = models.FloatField(default=0)
    total_assets = models.FloatField(default=0)
    total_current_assets = models.FloatField(default=0)
    total_current_liabilities = models.FloatField(default=0)
    total_deposits = models.FloatField(default=0)
    total_equity = models.FloatField(default=0)
    total_inventories = models.FloatField(default=0)
    total_liabilities = models.FloatField(default=0)
    total_long_term_assets = models.FloatField(default=0)
    total_long_term_liabilities = models.FloatField(default=0)
    total_receivables = models.FloatField(default=0)
    total_stockholders_equity = models.FloatField(default=0)
    total_tax_payable = models.FloatField(default=0)
    treasury_stock = models.FloatField(default=0)
    unearned_income = models.FloatField(default=0)
    unearned_premiums = models.FloatField(default=0)
    unpaid_loss_and_loss_reserve = models.FloatField(default=0)
    # Income Statement
    cost_of_goods_sold = models.FloatField(default=0)
    credit_losses_provision = models.FloatField(default=0)
    depreciation_and_depletion_and_amortization = models.FloatField(default=0)
    ebit = models.FloatField(default=0)
    ebitda = models.FloatField(default=0)
    eps_basic = models.FloatField(default=0)
    eps_diluted = models.FloatField(default=0)
    fees_and_other_income = models.FloatField(default=0)
    general_and_administrative_expense = models.FloatField(default=0)
    gross_profit = models.FloatField(default=0)
    interest_expense = models.FloatField(default=0)
    interest_income = models.FloatField(default=0)
    net_income = models.FloatField(default=0)
    net_income_continuing_operations = models.FloatField(default=0)
    net_income_discontinued_operations = models.FloatField(default=0)
    net_income_including_noncontrolling_interests = models.FloatField(default=0)
    net_interest_income = models.FloatField(default=0)
    net_interest_income_for_banks = models.FloatField(default=0)
    net_investment_income = models.FloatField(default=0)
    net_policyholder_benefits_or_claims = models.FloatField(default=0)
    non_interest_income = models.FloatField(default=0)
    non_operation_income = models.FloatField(default=0)
    operating_income = models.FloatField(default=0)
    other_expense = models.FloatField(default=0)
    other_income = models.FloatField(default=0)
    other_income_minority_interest = models.FloatField(default=0)
    other_net_income_or_loss = models.FloatField(default=0)
    other_noninterest_expense = models.FloatField(default=0)
    other_operating_expense = models.FloatField(default=0)
    policy_acquisition_expense = models.FloatField(default=0)
    pretax_income = models.FloatField(default=0)
    preferred_dividends = models.FloatField(default=0)
    research_and_development = models.FloatField(default=0)
    revenue = models.FloatField(default=0)
    selling_and_marketing_expense = models.FloatField(default=0)
    selling_and_general_and_administrative_expense = models.FloatField(default=0)
    shares_outstanding_basic_average = models.FloatField(default=0)
    shares_outstanding_diluted_average = models.FloatField(default=0)
    special_charges = models.FloatField(default=0)
    tax_expense = models.FloatField(default=0)
    tax_provision = models.FloatField(default=0)
    tax_rate = models.FloatField(default=0)
    total_expenses = models.FloatField(default=0)
    total_noninterest_expense = models.FloatField(default=0)
    total_operating_expense = models.FloatField(default=0)
    total_premiums_earned = models.FloatField(default=0)
    # Cashflow Statement
    all_taxes_paid = models.FloatField(default=0)
    asset_impairment_charge = models.FloatField(default=0)
    beginning_cash_position = models.FloatField(default=0)
    capital_expenditure = models.FloatField(default=0)
    cash_flow_for_dividends = models.FloatField(default=0)
    cash_flow_for_lease_financing = models.FloatField(default=0)
    cash_flow_from_discontinued_operations = models.FloatField(default=0)
    cash_flow_from_financing = models.FloatField(default=0)
    cash_flow_from_investing = models.FloatField(default=0)
    cash_flow_from_operations = models.FloatField(default=0)
    cash_flow_from_others = models.FloatField(default=0)
    cash_from_discontinued_investing_activities = models.FloatField(default=0)
    cash_from_discontinued_operating_activities = models.FloatField(default=0)
    cash_from_other_investing_activities = models.FloatField(default=0)
    cash_paid_for_insurance_activities = models.FloatField(default=0)
    cash_payments = models.FloatField(default=0)
    cash_payments_for_deposits_by_banks_and_customers = models.FloatField(default=0)
    cash_payments_for_loans = models.FloatField(default=0)
    cash_receipts_from_deposits_by_banks_and_customers = models.FloatField(default=0)
    cash_receipts_from_fees_and_commissions = models.FloatField(default=0)
    cash_receipts_from_loans = models.FloatField(default=0)
    cash_receipts_from_operating_activities = models.FloatField(default=0)
    cash_receipts_from_securities_related_activities = models.FloatField(default=0)
    cash_receipts_from_tax_refunds = models.FloatField(default=0)
    cash_receipts_from_insurance_activities = models.FloatField(default=0)
    change_in_inventory = models.FloatField(default=0)
    change_in_other_working_capital = models.FloatField(default=0)
    change_in_payables_and_accrued_expense = models.FloatField(default=0)
    change_in_prepaid_assets = models.FloatField(default=0)
    change_in_receivables = models.FloatField(default=0)
    change_in_working_capital = models.FloatField(default=0)
    deferred_tax = models.FloatField(default=0)
    depreciation_and_depletion_and_amortization_cash_flow = models.FloatField(default=0)
    dividends_paid = models.FloatField(default=0)
    dividends_received = models.FloatField(default=0)
    effect_of_exchange_rate_changes = models.FloatField(default=0)
    ending_cash_position = models.FloatField(default=0)
    ffo = models.FloatField(default=0)
    free_cash_flow = models.FloatField(default=0)
    interest_and_commission_paid = models.FloatField(default=0)
    interest_paid = models.FloatField(default=0)
    interest_received = models.FloatField(default=0)
    issuance_of_debt = models.FloatField(default=0)
    issuance_of_stock = models.FloatField(default=0)
    net_change_in_cash = models.FloatField(default=0)
    net_income_from_continuing_operations = models.FloatField(default=0)
    net_intangibles_purchase_and_sale = models.FloatField(default=0)
    net_issuance_of_debt = models.FloatField(default=0)
    net_issuance_of_preferred_stock = models.FloatField(default=0)
    other_cash_payments_from_operating_activities = models.FloatField(default=0)
    other_cash_receipts_from_operating_activities = models.FloatField(default=0)
    other_financing = models.FloatField(default=0)
    payments_of_debt = models.FloatField(default=0)
    payments_on_behalf_of_employees = models.FloatField(default=0)
    payments_to_suppliers_for_goods_and_services = models.FloatField(default=0)
    purchase_of_business = models.FloatField(default=0)
    purchase_of_investment = models.FloatField(default=0)
    purchase_of_property_and_plant_and_equipment = models.FloatField(default=0)
    receipts_from_customers = models.FloatField(default=0)
    receipts_from_government_grants = models.FloatField(default=0)
    repurchase_of_stock = models.FloatField(default=0)
    sale_of_business = models.FloatField(default=0)
    sale_of_investment = models.FloatField(default=0)
    sale_of_property_and_plant_and_equipment = models.FloatField(default=0)
    stock_based_compensation = models.FloatField(default=0)
    taxes_refund_paid = models.FloatField(default=0)
    # Additional Info
    total_employees_figure = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.company} - {self.quarter} - {self.year}'

    class Meta:
        ordering = ['-year', '-quarter']


class Country(models.Model):
    name = models.CharField(max_length=255)
    name_genitive = models.CharField(max_length=255)
    name_iso = models.CharField(max_length=10)
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    flag_icon = models.ImageField(upload_to='countries/flags', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_flag_url(self):
        if self.flag_icon:
            return URL_PREFIX + self.flag_icon.url
        return ''

    class Meta:
        ordering = ['name']

        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Sorter(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    order_type = models.CharField(max_length=255)
    reverse = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class CandlePerDay(models.Model):
    company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name='candles')
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    time = models.DateTimeField()
    is_complete = models.BooleanField()

    class Meta:
        ordering = ['time']

        verbose_name = 'Candle Per Day'
        verbose_name_plural = 'Candles Per Day'


class Currency(models.Model):
    name = models.CharField(max_length=255)
    name_iso = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Analyst(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class AnalystIdea(models.Model):
    analyst = models.ForeignKey('Analyst', on_delete=models.PROTECT)
    company = models.ForeignKey('Company', on_delete=models.PROTECT, related_name='analyst_ideas')
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
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='dividends')
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    scale = models.CharField(choices=SCALES, max_length=12)
    scale_unit = models.IntegerField(default=1)
    dividend_yield = models.FloatField()
    dividend_amount = models.FloatField()
    declared_date = models.DateField()
    ex_dividend_date = models.DateField()
    pay_date = models.DateField()
