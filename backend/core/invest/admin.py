from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe
from statements.services.analysis import check_has_financial_data


@admin.action(description='Analyse company by statements checks')
def check_company(modeladmin, request, queryset):
    return [check_has_financial_data(c) for c in queryset]


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'get_html_image',
        'market',
        'sector',
        'industry',
        'is_visible'
    )

    prepopulated_fields = {'slug': ('ticker',)}
    list_display_links = ('title',)
    list_editable = ('is_visible',)
    actions = [check_company]

    def get_html_image(self, object):
        if object.logo:
            return mark_safe(f'<img src="{object.logo.url}" width="50">')

    get_html_image.short_description = 'Logo'


@admin.register(models.Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'country')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'sector')
    list_display_links = ('title',)
    list_editable = ['sector']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('company', 'year', 'quarter', 'report_type', 'report_form')
    list_display_links = ('company',)


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency')


@admin.register(models.Sorter)
class SorterAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'order_type')


@admin.register(models.CandlePerDay)
class CandlePerDayAdmin(admin.ModelAdmin):
    list_display = ('company', 'open', 'high', 'close', 'low', 'volume', 'time', 'is_complete')
    ordering = ('-time', 'company__title')
    list_filter = ('company__title', 'time')
    search_fields = ('company__title', 'time')


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_iso', 'symbol')


@admin.register(models.Analyst)
class AnalystAdmin(admin.ModelAdmin):
    list_display = ('name', 'score')


@admin.register(models.AnalystIdea)
class AnalystIdea(admin.ModelAdmin):
    list_display = ('analyst', 'company', 'idea_created', 'price_target', 'date_target')
