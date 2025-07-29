from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Portfolio, PortfolioCompany


@admin.register(Portfolio)
class PortfolioAdmin(ModelAdmin):
    list_display = ('name', 'created', 'updated', 'user')


@admin.register(PortfolioCompany)
class PortfolioCompanyAdmin(ModelAdmin):
    list_display = ('company', 'portfolio', 'average_price', 'currency', 'share_amount')
