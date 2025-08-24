import datetime
from typing import List, Tuple

from django.conf import settings
from django.contrib.auth.models import User
from import_export import resources, fields, widgets

from apps.invest.models import Company, Country, Sector, Industry, SectorGroup, City


def add_translations(instance, row, model_fields: List | Tuple):
    for lang_code, _ in settings.LANGUAGES:
        translation = instance.translations.filter(language_code=lang_code).first()
        if not translation:
            translation = instance.translations.create(language_code=lang_code)

        translations_fields = {field: row.get(f'{field}_{lang_code}', '') for field in model_fields}

        for field, value in translations_fields.items():
            setattr(translation, field, value)

        translation.save()

class CompanyResource(resources.ModelResource):
    country = fields.Field(
        attribute='country',
        widget=widgets.ForeignKeyWidget(Country, 'iso_code')
    )
    city = fields.Field(
        attribute='city',
        widget=widgets.ForeignKeyWidget(City, 'geoname_id')
    )
    sector_group = fields.Field(
        attribute='sector_group',
        widget=widgets.ForeignKeyWidget(SectorGroup, 'slug')
    )
    sector = fields.Field(
        attribute='sector',
        widget=widgets.ForeignKeyWidget(Sector, 'slug')
    )
    industry = fields.Field(
        attribute='industry',
        widget=widgets.ForeignKeyWidget(Industry, 'slug')
    )
    created_by = fields.Field(
        attribute='created_by',
        widget=widgets.ForeignKeyWidget(User, 'id')
    )
    updated_by = fields.Field(
        attribute='updated_by',
        widget=widgets.ForeignKeyWidget(User, 'id')
    )

    class Meta:
        model = Company
        skip_unchanged = True
        report_skipped = True
        fields = (
            'country',
            'sector_group',
            'sector',
            'industry',
            'is_visible',
            'is_fund',
            'website',
            'year_founded',
            'title',
            'short_title',
            'short_title_genitive',
            'description',
            'short_description',
            'city',
            'created',
            'updated',
            'created_by',
            'updated_by',
            'is_verified',
        )

    def before_import_row(self, row, **kwargs):
        row['created'] = datetime.datetime.now(datetime.timezone.utc)
        row['updated'] = datetime.datetime.now(datetime.timezone.utc)
        user = kwargs.get('user')
        row['created_by'] = user.id
        row['updated_by'] = user.id
        row['is_visible'] = False
        row['is_verified'] = False

    def after_save_instance(self, instance, row, **kwargs):
        model_fields = ('title', 'short_title', 'short_title_genitive', 'description', 'short_description')
        add_translations(instance, row, model_fields)


class CityResource(resources.ModelResource):
    country = fields.Field(
        attribute='country',
        widget=widgets.ForeignKeyWidget(Country, 'iso_code')
    )

    class Meta:
        model = City
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('geoname_id',)
        fields = ('name', 'geoname_id', 'locode_id', 'country')

    def after_save_instance(self, instance, row, **kwargs):
        model_fields = ('name',)
        add_translations(instance, row, model_fields)
