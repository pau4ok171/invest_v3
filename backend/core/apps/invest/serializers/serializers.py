import time

from rest_framework import serializers

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from apps.invest import models


class CurrencySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=models.Currency)

    class Meta:
        model = models.Currency
        fields = (
            'iso_code',
            'symbol',
            'translations',
        )


class CountrySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=models.Country)

    class Meta:
        model = models.Country
        fields = (
            'iso_code',
            'translations',
        )


class SectorSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=models.Sector)

    class Meta:
        model = models.Sector
        fields = (
            'slug',
            'main_header',
            'translations',
        )


class SectorWithCountriesSerializer(TranslatableModelSerializer):
    """
    Serializer for sector filter options with country availability.
    Returns sectors along with countries where they have instruments,
    enabling dynamic filter UI where only relevant sectors are shown
    based on selected country.
    """
    translations = TranslatedFieldsField(shared_model=models.Sector)
    countries_iso = serializers.SerializerMethodField()

    class Meta:
        model = models.Sector
        fields = (
            'id',
            'slug',
            'countries_iso',
            'translations',
        )

    @staticmethod
    def get_countries_iso(instance: models.Sector):
        return (
            models.Country.objects
            .filter(exchanges__instruments__company__sector__pk=instance.pk)
            .distinct()
            .order_by('iso_code')
            .values_list('iso_code', flat=True)
        )


class ExchangePerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExchangePerformance
        fields = (
            'return_7d',
            'return_30d',
            'return_90d',
            'return_1y',
            'return_3y',
            'return_5y',
            'average_weekly_mouvement',
            'volatility_10p',
            'volatility_90p',
        )


class ExchangeSerializer(serializers.ModelSerializer):
    performance = ExchangePerformanceSerializer(read_only=True)

    class Meta:
        model = models.Exchange
        fields = (
            'title',
            'performance',
        )


class SectorExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SectorExchange
        fields = (
            'return_7d',
            'return_30d',
            'return_90d',
            'return_1y',
            'return_3y',
            'return_5y',
            'average_weekly_mouvement',
        )


class ReportSerializer(serializers.ModelSerializer):
    updated = serializers.SerializerMethodField()

    class Meta:
        model = models.ReportMetadata
        fields = (
            'updated',
            'total_employees_figure',
            'share_outstanding_eop',
            'scale',
            'scale_unit',
        )

    @staticmethod
    def get_updated(instance: models.ReportMetadata):
        return instance.updated.strftime('%d %b, %Y')


class AnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Analyst
        fields = '__all__'


class AnalystIdeaSerializer(serializers.ModelSerializer):
    analyst = AnalystSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = models.AnalystIdea
        fields = '__all__'


class CandleSerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField()

    class Meta:
        model = models.Candle
        fields = ('time', 'close')

    @staticmethod
    def get_time(instance: models.Candle):
        return time.mktime(instance.time.timetuple()) * 1000


class DividendSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = models.Dividend
        fields = (
            'currency',
            'dividend_net',
            'payment_date',
            'declared_date',
            'ex_dividend_date',
            'dividend_type',
            'record_date',
            'regularity',
            'close_price',
            'yield_value',
        )
