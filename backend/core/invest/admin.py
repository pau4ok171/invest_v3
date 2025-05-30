import datetime

from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe
from statements.services.analysis import main

from parler.admin import TranslatableAdmin


@admin.action(description='Analyse company by statements checks')
def check_company(modeladmin, request, queryset):
    return main(queryset)


@admin.register(models.Sector)
class SectorAdmin(TranslatableAdmin):
    list_display = ('id', '__str__', 'slug')
    list_display_links = ('__str__',)


@admin.register(models.Company)
class CompanyAdmin(TranslatableAdmin):
    list_display = (
        'id',
        '__str__',
        'slug',
        'get_html_image',
        'market',
        'sector',
        'industry',
        'is_visible'
    )

    list_display_links = ('__str__',)
    list_editable = ('is_visible',)
    readonly_fields = ('created', 'updated', 'created_by', 'updated_by')
    actions = [check_company]

    def get_html_image(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="50">')

    get_html_image.short_description = 'Logo'

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
            obj.updated = datetime.datetime.utcnow()
        else:
            obj.created_by = request.user
            obj.created = datetime.datetime.utcnow()

        super().save_model(request, obj, form, change)


@admin.register(models.Industry)
class IndustryAdmin(TranslatableAdmin):
    list_display = ('id', '__str__', 'slug', 'sector')
    list_display_links = ('__str__',)
    list_editable = ['sector']


@admin.register(models.Country)
class CountryAdmin(TranslatableAdmin):
    list_display = ('id', '__str__', 'currency')


@admin.register(models.Currency)
class CurrencyAdmin(TranslatableAdmin):
    list_display = ('__str__', 'iso_code', 'symbol')


@admin.register(models.Analyst)
class AnalystAdmin(TranslatableAdmin):
    list_display = ('__str__', 'score')


@admin.register(models.Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'country')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class BalanceSheetInline(admin.StackedInline):
    model = models.BalanceSheet
    extra = 0


class IncomeStatementInline(admin.StackedInline):
    model = models.IncomeStatement
    extra = 0


class CashflowStatementInline(admin.StackedInline):
    model = models.CashflowStatement
    extra = 0


@admin.register(models.ReportMetadata)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'quarter', 'report_period_type', 'report_form')
    list_display_links = ('company',)
    fieldsets = (
        ('', {
            'fields':
                [
                    'company',
                    'verified',
                    'is_analysed',
                    'is_automatically_collected',
                    'is_verified',
                    'is_complete',
                ]
        }),
        ('Summary', {
            'fields':
                [
                    'year',
                    'quarter',
                    'report_period_type',
                    'report_form',
                    'scale',
                    'scale_unit',
                    'currency',
                ]
        }),
        ('Additional Info', {
            'fields':
                [
                    'share_outstanding_eop',
                    'total_employees_figure',
                ]
        }),

    )

    inlines = [
        BalanceSheetInline,
        IncomeStatementInline,
        CashflowStatementInline,
    ]


@admin.register(models.CandlePerDay)
class CandlePerDayAdmin(admin.ModelAdmin):
    list_display = ('get_company_title', 'open', 'high', 'close', 'low', 'volume', 'time', 'is_complete')
    ordering = ('-time', 'company__translations__title')
    list_filter = ('company', 'time')
    search_fields = ('company__translations__title', 'time')

    def get_company_title(self, obj):
        return obj.company.safe_translation_getter('title', any_language=True)
    get_company_title.short_description = 'Company Title'
    get_company_title.admin_order_field = 'company__translations__title'


@admin.register(models.AnalystIdea)
class AnalystIdeaAdmin(admin.ModelAdmin):
    list_display = ('analyst', 'company', 'idea_created', 'price_target', 'date_target')


@admin.register(models.Dividend)
class DividendAdmin(admin.ModelAdmin):
    list_display = ('company', 'ex_dividend_date', 'dividend_yield')
