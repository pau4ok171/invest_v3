from django.contrib import admin
from .models import Statement


@admin.register(Statement)
class StatementAdmin(admin.ModelAdmin):
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
