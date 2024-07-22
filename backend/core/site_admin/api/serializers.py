from django.conf import settings

from rest_framework import serializers

from invest.models import Company


URL_PREFIX = settings.URL_PREFIX


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
    market_name = serializers.SerializerMethodField('get_market_name')
    sector_name = serializers.SerializerMethodField('get_sector_name')
    industry_name = serializers.SerializerMethodField('get_industry_name')
    country_flag = serializers.SerializerMethodField('get_country_flag')
    currency_symbol = serializers.SerializerMethodField('get_currency_symbol')
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
            'industry_name',
            'absolute_url',
            'country_flag',
            'currency_symbol',
            'created',
            'updated',
        )

    @staticmethod
    def get_market_name(instance):
        return instance.market.title

    @staticmethod
    def get_sector_name(instance):
        return instance.sector.title

    @staticmethod
    def get_industry_name(instance):
        return instance.industry.title

    @staticmethod
    def get_country_flag(instance):
        icon = instance.country.flag_icon
        return icon.url if icon else ''

    @staticmethod
    def get_currency_symbol(instance):
        return instance.country.currency.symbol

