from django.conf import settings
from django.contrib import admin, messages

from apps.statements.services.analysis import main


@admin.action(description='Analyse company by statements checks')
def check_company(modeladmin, request, queryset):
    return main(queryset)


@admin.action(description='Validate company and set company is_public')
def validate_company(modeladmin, request, queryset):
    checks = {
        'total': queryset.count(),
        'valid': 0,
        'no_statements': 0,
        'no_candles': 0,
        'no_translations': 0,
        'no_instruments': 0,
    }

    for company in queryset:
        is_valid = True

        # Statements
        if not company.statements.exists():
            is_valid = False
            checks['no_statements'] += 1

        # Instruments
        instrument = company.instruments.filter(instrument_type='share').first()
        if not instrument:
            is_valid = False
            checks['no_instruments'] += 1
            checks['no_candles'] += 1
        # Candles
        elif not instrument.candles.exists():
            is_valid = False
            checks['no_candles'] += 1

        # Translations
        if not company.is_verified:
            is_valid = False
            checks['no_translations'] += 1

        company.is_visible = is_valid
        company.save()
        if is_valid:
            checks['valid'] += 1

    report = (
        f'Companies checked: {checks["total"]}',
        f'✔ Valid: {checks["valid"]}',
        f'✖ Problems:',
        f' - No statements: {checks["no_statements"]}',
        f' - No instruments: {checks["no_instruments"]}',
        f' - No candles: {checks["no_candles"]}',
        f' - No translations: {checks["no_translations"]}',
    )

    if checks['valid'] == checks['total']:
        messages.success(request, f'All companies was validated!{report}')
    else:
        messages.warning(request, report)


@admin.action(description='Check if all needed translations was set')
def check_company_translation(modeladmin, request, queryset):
    for company in queryset:
        is_valid = True
        for lang_code, _ in settings.LANGUAGES:
            company.set_current_language(lang_code)
            if not company.title:
                is_valid = False
            if not company.short_title:
                is_valid = False
            if not company.short_title_genitive:
                is_valid = False
            if not company.description:
                is_valid = False

        company.is_verified = is_valid
        company.save()