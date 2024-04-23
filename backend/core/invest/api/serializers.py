import time

from dateutil.relativedelta import relativedelta
from rest_framework import serializers
from rest_framework.fields import empty

from invest.models import Company, Country, Sector, Market, CandlePerDay, Sorter, Report, AnalystIdea, Analyst, Currency


class CountrySerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    slug = serializers.SlugField(source='name_iso')

    class Meta:
        model = Country
        fields = (
            'id',
            'title',
            'slug',
            'currency',
            'markets',
        )
        depth = 1


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['title', 'slug']


class SectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = (
            'title',
            'slug',
            'main_header'
        )


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['title']


class PriceDataSerialize(serializers.ModelSerializer):
    class Meta:
        model = CandlePerDay
        fields = '__all__'


class CompanySearchSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    market = MarketSerializer(read_only=True)
    sector = SectorSerializer(read_only=True)
    logo_url = serializers.CharField(source='get_logo', read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Company
        fields = (
            'uid',
            'title',
            'logo_url',
            'country',
            'sector',
            'market',
            'absolute_url',
        )


class CompanySerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    market = MarketSerializer(read_only=True)
    sector = SectorSerializer(read_only=True)
    logo_url = serializers.CharField(source='get_logo', read_only=True)
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    is_watchlisted = serializers.SerializerMethodField('get_is_watchlisted')
    price_data = serializers.SerializerMethodField('get_price_data')

    class Meta:
        model = Company
        fields = (
            'uid',
            'ticker',
            'title',
            'logo_url',
            'country',
            'market',
            'sector',
            'absolute_url',
            'is_watchlisted',
            'price_data',
        )

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.candles = None

    def get_is_watchlisted(self, instance) -> bool:
        user = self.context['request'].user
        if not user.is_anonymous:
            return user.companies_watchlisted.filter(pk__exact=instance.id).exists()
        return False

    def get_price_data(self, instance):
        self.get_candles(instance)
        if self.candles:
            return {
                "last_price": self.get_last_price(instance),
                "return_7d": self.get_return_7d(instance),
                "return_1y": self.get_return_1y(instance),
                "capitalisation": self.get_capitalisation(instance),
            }
        return {
            "last_price": 0,
            "return_7d": 0,
            "return_1y": 0,
            "capitalisation": 0,
        }

    def get_last_price(self, instance):
        if self.candles is None:
            self.get_candles(instance)
        return self.candles.latest("time").close or 0

    def get_return_7d(self, instance):
        if self.candles is None:
            self.get_candles(instance)

        return self.get_closest_available_return(days=7)

    def get_return_1y(self, instance):
        if self.candles is None:
            self.get_candles(instance)

        return self.get_closest_available_return(years=1)

    def get_capitalisation(self, instance):
        if self.candles is None:
            self.get_candles(instance)

        report = Report.objects.filter(company__pk=instance.id)
        share_outstanding = report.latest('year', 'quarter').share_outstanding if report else None

        return self.candles.latest("time").close * share_outstanding if share_outstanding else 0

    def get_candles(self, instance):
        if CandlePerDay.objects.filter(company__pk=instance.id).exists():
            self.candles = CandlePerDay.objects.filter(company__pk=instance.id)
        else:
            self.candles = None

    def get_closest_available_return(self, *args, **kwargs):
        last_price = self.candles.latest('time').close
        last_time = self.candles.latest('time').time
        past_time = last_time - relativedelta(**kwargs)

        past_price = self.candles.filter(time__lte=past_time).order_by('-time') or None

        if past_price:
            past_price = past_price.first().close
            return (last_price - past_price) / past_price * 100
        return 0


class ReportSerializer(serializers.ModelSerializer):
    updated = serializers.SerializerMethodField('get_updated')

    class Meta:
        model = Report
        fields = (
            'updated',
            'total_employees_figure',
                  )

    def get_updated(self, instance):
        return instance.updated.strftime('%d %b, %Y')


class AnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyst
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class AnalystIdeaSerializer(serializers.ModelSerializer):
    analyst = AnalystSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = AnalystIdea
        fields = '__all__'


class CompanyDetailSerializer(CompanySerializer):
    sector = SectorDetailSerializer(read_only=True)
    reports = ReportSerializer(many=True)
    analyst_ideas = AnalystIdeaSerializer(many=True)

    class Meta:
        model = Company
        fields = (
            'id',
            'uid',
            'ticker',
            'title',
            'slug',
            'description',
            'short_description',
            'year_founded',
            'website',
            'logo_url',
            'country',
            'market',
            'sector',
            'absolute_url',
            'is_watchlisted',
            'price_data',
            'reports',
            'analyst_ideas',
        )


class CandlePerDaySerializer(serializers.ModelSerializer):
    time = serializers.SerializerMethodField('get_timestamp')

    class Meta:
        model = CandlePerDay
        fields = ['time', 'close']

    @staticmethod
    def get_timestamp(obj):
        return time.mktime(obj.time.timetuple()) * 1000


class CompanyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandlePerDaySerializer
        fields = '__all__'


class SorterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sorter
        fields = '__all__'
