from django.contrib import admin
from .models import Portfolio, PortfolioCompany


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated', 'user')


@admin.register(PortfolioCompany)
class PortfolioCompanyAdmin(admin.ModelAdmin):
    list_display = ('company', 'portfolio', 'average_price', 'currency', 'share_amount')
