import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe

from unfold.admin import ModelAdmin, StackedInline
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget, UnfoldAdminTextareaWidget

from . import models

from statements.services.analysis import main

from parler.admin import TranslatableAdmin

from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass


@admin.action(description='Analyse company by statements checks')
def check_company(modeladmin, request, queryset):
    return main(queryset)


@admin.register(models.Sector)
class SectorAdmin(TranslatableAdmin, ModelAdmin):
    list_display = ('id', 'get_title', 'slug')
    list_display_links = ('get_title',)
    search_fields = ('translations__title', 'slug')
    ordering = ['id']

    fieldsets = (
        ('General', {
            'fields': (
                'slug',
                'main_header',
            ),
        }),
        ('Translations', {
            'fields': (
                'title',
                'description',
            )
        }),
    )

    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
    get_title.short_description = 'Title'
    get_title.admin_order_field = 'translations__title'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget = UnfoldAdminTextInputWidget()
        form.base_fields['description'].widget = UnfoldAdminTextareaWidget()
        return form


class CompanyPerformanceInline(StackedInline):
    model = models.CompanyPerformance
    extra = 0


@admin.register(models.Company)
class CompanyAdmin(TranslatableAdmin, ModelAdmin):
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

    inlines = [
        CompanyPerformanceInline,
    ]

    fieldsets = (
        ('General', {
            'fields': (
                'ticker',
                'slug',
                'uid',
                'country',
                'market',
                'sector',
                'industry',
                'created',
                'updated',
                'is_visible',
                'logo',
                'is_fund',
                'website',
                'year_founded',
                'created_by',
                'updated_by',
            ),
        }),
        ('Translations', {
            'fields': (
                'title',
                'short_title',
                'short_title_genitive',
                'description',
                'short_description',
                'city',
             )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget = UnfoldAdminTextInputWidget()
        form.base_fields['short_title'].widget = UnfoldAdminTextInputWidget()
        form.base_fields['short_title_genitive'].widget = UnfoldAdminTextInputWidget()
        form.base_fields['description'].widget = UnfoldAdminTextareaWidget()
        form.base_fields['short_description'].widget = UnfoldAdminTextareaWidget()
        form.base_fields['city'].widget = UnfoldAdminTextInputWidget()
        return form

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
class IndustryAdmin(TranslatableAdmin, ModelAdmin):
    list_display = ('id', '__str__', 'slug', 'sector')
    list_display_links = ('__str__',)
    list_editable = ['sector']
    ordering = ['id']

    fieldsets = (
        ('General', {
            'fields': (
                'slug',
                'sector',
            ),
        }),
        ('Translations', {
            'fields': (
                'title',
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget = UnfoldAdminTextInputWidget()
        return form


@admin.register(models.Country)
class CountryAdmin(TranslatableAdmin, ModelAdmin):
    list_display = ('id', '__str__', 'currency')
    ordering = ['id']

    fieldsets = (
        ('General', {
            'fields': (
                'iso_code',
                'currency',
            ),
        }),
        ('Translations', {
            'fields': (
                'name',
                'name_genitive',
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].widget = UnfoldAdminTextInputWidget()
        form.base_fields['name_genitive'].widget = UnfoldAdminTextInputWidget()
        return form


@admin.register(models.Currency)
class CurrencyAdmin(TranslatableAdmin, ModelAdmin):
    list_display = ('__str__', 'iso_code', 'symbol')

    fieldsets = (
        ('General', {
            'fields': (
                'iso_code',
                'symbol',
            ),
        }),
        ('Translations', {
            'fields': (
                'name',
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].widget = UnfoldAdminTextInputWidget()
        return form


@admin.register(models.Analyst)
class AnalystAdmin(TranslatableAdmin, ModelAdmin):
    list_display = ('__str__', 'score')
    ordering = ['id']

    fieldsets = (
        ('General', {
            'fields': (
                'score',
            ),
        }),
        ('Translations', {
            'fields': (
                'name',
                'description',
            )
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['name'].widget = UnfoldAdminTextInputWidget()
        form.base_fields['description'].widget = UnfoldAdminTextareaWidget()
        return form


class MarketPerformanceInline(StackedInline):
    model = models.MarketPerformance
    extra = 0


@admin.register(models.Market)
class MarketAdmin(ModelAdmin):
    list_display = ('id', 'title', 'slug', 'country')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    inlines = [
        MarketPerformanceInline,
    ]


class BalanceSheetInline(StackedInline):
    model = models.BalanceSheet
    extra = 0


class IncomeStatementInline(StackedInline):
    model = models.IncomeStatement
    extra = 0


class CashflowStatementInline(StackedInline):
    model = models.CashflowStatement
    extra = 0


@admin.register(models.ReportMetadata)
class ReportAdmin(ModelAdmin):
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
class CandlePerDayAdmin(ModelAdmin):
    list_display = ('get_company_title', 'open', 'high', 'close', 'low', 'volume', 'time', 'is_complete')
    ordering = ('-time', 'company__id')
    list_filter = ('company', 'time')
    search_fields = ('company__translations__title', 'time')

    def get_company_title(self, obj):
        return obj.company.safe_translation_getter('title', any_language=True)
    get_company_title.short_description = 'Company Title'
    get_company_title.admin_order_field = 'company__id'


@admin.register(models.AnalystIdea)
class AnalystIdeaAdmin(ModelAdmin):
    list_display = ('analyst', 'company', 'idea_created', 'price_target', 'date_target')


@admin.register(models.Dividend)
class DividendAdmin(ModelAdmin):
    list_display = ('company', 'ex_dividend_date', 'dividend_yield')
