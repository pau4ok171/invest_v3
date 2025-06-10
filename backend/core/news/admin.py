from django.contrib import admin

from unfold.admin import ModelAdmin

from news.models import News


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = (
        'company',
        'date',
        'type',
    )
