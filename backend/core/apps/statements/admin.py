from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import Statement


@admin.register(Statement)
class StatementAdmin(ModelAdmin):
    list_display = (
        'name',
        'company',
        'type',
        'status',
    )
    list_filter = (
        'name',
        'company',
        'type',
        'area',
        'status',
    )
