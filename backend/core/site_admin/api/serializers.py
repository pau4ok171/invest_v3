from django.conf import settings

from rest_framework import serializers

from invest.models import Company, Country, Industry, Market, Sector, Currency

URL_PREFIX = settings.URL_PREFIX


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'name',
            'symbol',
        )


class CountrySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    flag_url = serializers.CharField(source='get_flag_url', read_only=True)

    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'name_iso',
            'currency',
            'flag_url',
        )


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = (
            'title',
            'slug',
            'sector',
        )


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = (
            'title',
            'slug',
            'country',
        )


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = (
            'id',
            'title',
            'slug',
        )


class CompaniesSerializer(serializers.ModelSerializer):
    market_name = serializers.SerializerMethodField('get_market_name')
    sector_name = serializers.SerializerMethodField('get_sector_name')
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Company
        fields = (
            'id',
            'ticker',
            'slug',
            'uid',
            'title',
            'short_title',
            'is_visible',
            'logo',
            'is_fund',
            'market_name',
            'sector_name',
            'absolute_url',
        )

    @staticmethod
    def get_market_name(instance):
        return instance.market.title

    @staticmethod
    def get_sector_name(instance):
        return instance.sector.title


class CompanySerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    industry = IndustrySerializer()
    market = MarketSerializer()
    sector = SectorSerializer()

    class Meta:
        model = Company
        fields = (
            'ticker',
            'slug',
            'uid',
            'title',
            'short_title',
            'short_title_genitive',
            'description',
            'short_description',
            'city',
            'country',
            'market',
            'sector',
            'industry',
            'created',
            'updated',
            'is_visible',
            'logo',
            'is_fund',
            'website',
            'year_founded',
        )
