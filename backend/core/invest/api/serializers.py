import time

from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from invest.models import Company, Country, Sector, Market, CandlePerDay


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['title']


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['title']


class CompanySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    market = MarketSerializer(read_only=True)
    sector = SectorSerializer(read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Company
        fields = ['ticker', 'title', 'logo', 'country', 'market', 'sector', 'absolute_url']


class CandlePerDaySerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('get_timestamp')

    class Meta:
        model = CandlePerDay
        fields = ['time', 'close']

    @staticmethod
    def get_timestamp(obj):
        return time.mktime(obj.time.timetuple()) * 1000
