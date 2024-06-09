from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from .model_choices import QUARTERS, REPORT_TYPES, REPORT_FORMS, SCALES
from notes.models import Note

URL_PREFIX = settings.URL_PREFIX


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
    logo = models.ImageField(upload_to='companies/logos/small', blank=True, default='companies/logos/small/default.png')
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
    # Balance
    equity = models.FloatField()
    current_liabilities = models.FloatField()
    non_current_liabilities = models.FloatField()
    liabilities = models.FloatField()
    debt = models.FloatField()
    cash = models.FloatField()
    net_debt = models.FloatField()
    assets = models.FloatField()
    # Revenues
    sales = models.FloatField()
    cost_of_sales = models.FloatField()
    gross_margin = models.FloatField()
    operation_expenses = models.FloatField()
    operation_income = models.FloatField()
    other_income_net = models.FloatField()
    income_before_taxes = models.FloatField()
    taxes = models.FloatField()
    income_net = models.FloatField()
    amortisation = models.FloatField()
    capex = models.FloatField()
    # Additional Info
    total_employees_figure = models.IntegerField(null=True)
    share_outstanding = models.IntegerField(help_text='Pieces')

    def __str__(self):
        return f'{self.company} - {self.quarter} - {self.year}'

    class Meta:
        ordering = ['-year', '-quarter']


class Country(models.Model):
    name = models.CharField(max_length=255)
    name_genitive = models.CharField(max_length=255)
    name_iso = models.CharField(max_length=10)
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    # TODO: add flag_icon for each country

    def __str__(self):
        return self.name

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
