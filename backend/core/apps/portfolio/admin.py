from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Portfolio, PortfolioPosition


@admin.register(Portfolio)
class PortfolioAdmin(ModelAdmin):
    list_display = ('name', 'created', 'updated', 'user')


@admin.register(PortfolioPosition)
class PortfolioPositionAdmin(ModelAdmin):
    list_display = ('instrument', 'portfolio', 'average_price', 'currency', 'share_amount')
