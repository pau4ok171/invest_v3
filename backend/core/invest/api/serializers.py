import time

from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from rest_framework import serializers
from rest_framework.fields import empty

from invest.models import Company, Country, Sector, Market, CandlePerDay, Sorter, Report, AnalystIdea, Analyst, \
    Currency, Dividend, SectorMarket
from statements.models import Statement
from statements.api.serializers import StatementSerializer
from statements.types import Area, Status
from news.api.serializers import NewsSerializer


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
    countries = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = (
            'id',
            'title',
            'slug',
            'countries',
        )

    @staticmethod
    def get_countries(obj):
        countries = Country.objects.filter(company__sector=obj).distinct()
        return CountrySerializer(countries, many=True).data


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
        fields = (
            'title',
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


class SectorMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorMarket
        fields = (
            'return_7d',
            'return_30d',
            'return_90d',
            'return_1y',
            'return_3y',
            'return_5y',
            'average_weekly_mouvement',
        )


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
            'ticker',
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
    formatting = serializers.SerializerMethodField('get_formatting')
    statements = serializers.SerializerMethodField('get_statements')

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
            'price_data',
            'formatting',
            'updated',
            'return_7d',
            'return_30d',
            'return_90d',
            'return_1y',
            'return_3y',
            'return_5y',
            'statements',
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
                "capitalisation": self.get_capitalisation(instance),
            }
        return {
            "last_price": 0,
            "capitalisation": 0,
        }

    def get_last_price(self, instance):
        if self.candles is None:
            self.get_candles(instance)
        return self.candles.latest("time").close or 0

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

    @staticmethod
    def get_statements(instance):
        statements = Statement.objects.filter(company=instance)
        return StatementSerializer(statements, many=True).data

    @staticmethod
    def get_formatting(obj):
        return {
            'primaryCurrencyISO': obj.country.currency.name_iso,
            'primaryCurrencySymbol': obj.country.currency.symbol,
            'reportCurrencyISO': '',
            'reportCurrencySymbol': '',
            'tradingCurrencyISO': '',
            'tradingCurrencySymbol': '',
        }


class ReportSerializer(serializers.ModelSerializer):
    updated = serializers.SerializerMethodField('get_updated')

    class Meta:
        model = Report
        fields = (
            'updated',
            'total_employees_figure',
            'share_outstanding',
            'scale',
            'scale_unit',
            'income_net',
            'equity',
            'debt',
            'sales',
            'cost_of_sales',
            'gross_margin',
            'operation_expenses',
            'operation_income',
            'other_income_net',
            'taxes',
            'assets',
        )

    @staticmethod
    def get_updated(instance):
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
    sector_market = serializers.SerializerMethodField('get_sector_market')
    reports = ReportSerializer(many=True)
    analyst_ideas = AnalystIdeaSerializer(many=True)
    formatting = serializers.SerializerMethodField('get_formatting')
    company_news = NewsSerializer(many=True)
    next_dividend = serializers.SerializerMethodField('get_next_dividend')

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
            'sector_market',
            'sector',
            'absolute_url',
            'is_watchlisted',
            'price_data',
            'reports',
            'analyst_ideas',
            'formatting',
            'company_news',
            'next_dividend',
            'last_reported_earnings',
            'next_earnings',
            'return_7d',
            'return_30d',
            'return_90d',
            'return_1y',
            'return_3y',
            'return_5y',
            'average_weekly_mouvement',
        )

    @staticmethod
    def get_formatting(obj):
        return {
            'primaryCurrencyISO': obj.country.currency.name_iso,
            'primaryCurrencySymbol': obj.country.currency.symbol,
            'reportCurrencyISO': '',
            'reportCurrencySymbol': '',
            'tradingCurrencyISO': '',
            'tradingCurrencySymbol': '',
        }

    @staticmethod
    def get_next_dividend(instance: Company):
        next_dividend = instance.dividends.filter(ex_dividend_date__gte=today())
        if next_dividend:
            next_dividend = next_dividend.latest('ex_dividend_date')
            return DividendSerializer(next_dividend).data
        return {}

    @staticmethod
    def get_sector_market(instance: Company):
        sector_market = SectorMarket.objects.get(market_id=instance.market.id, sector_id=instance.sector.id)
        return SectorMarketSerializer(sector_market).data


class CompanyPeersSerializer(CompanySerializer):
    sector = SectorDetailSerializer(read_only=True)
    formatting = serializers.SerializerMethodField('get_formatting')
    snowflake = serializers.SerializerMethodField('get_snowflake')

    class Meta:
        model = Company
        fields = (
            'id',
            'uid',
            'ticker',
            'title',
            'slug',
            'country',
            'market',
            'sector',
            'absolute_url',
            'price_data',
            'formatting',
            'snowflake',
        )

    @staticmethod
    def get_formatting(obj):
        return {
            'primaryCurrencyISO': obj.country.currency.name_iso,
            'primaryCurrencySymbol': obj.country.currency.symbol,
            'reportCurrencyISO': '',
            'reportCurrencySymbol': '',
            'tradingCurrencyISO': '',
            'tradingCurrencySymbol': '',
        }

    @staticmethod
    def get_snowflake(obj):
        statements = Statement.objects.filter(company=obj)
        return {
            "value": StatementSerializer(statements.filter(area=Area.VALUE, status=Status.PASS, outcome=1002), many=True).data,
            "future": StatementSerializer(statements.filter(area=Area.FUTURE, status=Status.PASS, outcome=1002), many=True).data,
            "past": StatementSerializer(statements.filter(area=Area.PAST, status=Status.PASS, outcome=1002), many=True).data,
            "health": StatementSerializer(statements.filter(area=Area.HEALTH, status=Status.PASS, outcome=1002), many=True).data,
            "dividends": StatementSerializer(statements.filter(area=Area.DIVIDENDS, status=Status.PASS, outcome=1002), many=True).data,
        }


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


class DividendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dividend
        fields = (
            'scale',
            'scale_unit',
            'dividend_yield',
            'dividend_amount',
            'declared_date',
            'ex_dividend_date',
            'pay_date',
            'currency',
        )
        depth = 1
