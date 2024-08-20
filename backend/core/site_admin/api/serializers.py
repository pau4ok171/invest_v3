from django.conf import settings
from django.contrib.auth.models import User

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
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
            'created_by',
            'updated_by',
            'is_visible',
            'logo',
            'is_fund',
            'website',
            'year_founded',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['country'] = CountrySerializer(instance.country).data
        response['industry'] = IndustrySerializer(instance.industry).data
        response['market'] = MarketSerializer(instance.market).data
        response['sector'] = SectorSerializer(instance.sector).data
        response['created_by'] = UserSerializer(instance.created_by).data
        response['updated_by'] = UserSerializer(instance.updated_by).data
        return response
