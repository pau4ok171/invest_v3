# Django
from django.db.models import Q

# DRF
from rest_framework import exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
# Invest App
from apps.invest import serializers

from apps.invest.paginators import StandardResultsSetPagination
from apps.invest.models import Company, Country, Sector, Currency, Instrument

######################################################################
# Companies
######################################################################
class CompanyListAPIView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.CompanySerializer

    def get_queryset(self):
        country_slug = self.request.query_params.get('country', 'global')
        sector_slug = self.request.query_params.get('sector', 'any')

        queryset = Company.objects.filter(
            is_visible=True
        ).select_related(
            'country',
            'sector',
            'country__currency'
        ).distinct()

        if not country_slug == 'global':
            queryset = queryset.filter(country__iso_code=country_slug)
        if not sector_slug == 'any':
            queryset = queryset.filter(sector__slug=sector_slug)

        return queryset


class CompanyDetailAPIView(RetrieveAPIView):
    queryset = (
        Company.objects
        .filter(is_visible=True)
        .select_related('country', 'sector', 'country__currency')
        .prefetch_related('analyst_idea', 'company_news')
    )
    serializer_class = serializers.CompanyFullSerializer
    lookup_field = 'uid'
    lookup_url_kwarg = 'uid'

######################################################################
# Countries
######################################################################
class CountryListAPIView(ListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        return (
            Country.objects
            .all()
            .prefetch_related('translations','currency')
            .order_by('iso_code')
        )

######################################################################
# Currencies
######################################################################
class CurrencyListAPIView(ListAPIView):
    serializer_class = serializers.CurrencySerializer
    queryset = (
        Currency.objects
        .all()
        .prefetch_related('translations')
        .order_by('iso_code')
    )

######################################################################
# Shares
######################################################################
class ShareListAPIView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.ShareSerializer

    def get_queryset(self):
        queryset = (
            Instrument.objects
            .filter(instrument_type='share', company__is_visible=True)
            .select_related(
                'company',
                'exchange',
                'currency',
                'company__country',
                'company__sector',
                'company__industry',
            )
        )

        country = self.request.query_params.get('country', 'global')
        sector = self.request.query_params.get('sector', 'any')

        if not country == 'global':
            queryset = queryset.filter(exchange__country__iso_code=country)
        if not sector == 'any':
            queryset = queryset.filter(company__sector__slug=sector)

        return queryset


class ShareListCountryListAPIView(ListAPIView):
    serializer_class = serializers.CountrySerializer

    def get_queryset(self):
        return (
            Country.objects
            .filter(
                exchanges__instruments__company__is_visible=True,
                exchanges__instruments__isnull=False,
                exchanges__instruments__instrument_type='share',
            )
            .prefetch_related('translations', 'currency')
            .distinct()
            .order_by('iso_code')
        )


class ShareListSectorListAPIView(ListAPIView):
    serializer_class = serializers.SectorWithCountriesSerializer

    def get_queryset(self):
        return (
            Sector.objects
            .filter(
                companies__is_visible=True,
                companies__instruments__isnull=False,
                companies__instruments__instrument_type='share',
            )
            .prefetch_related('translations')
            .distinct()
            .order_by('slug')
        )


class ShareListSearchListAPIView(ListAPIView):
    serializer_class = serializers.ShareSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('query', '').strip()
        limit = self.request.query_params.get('limit', '10').strip()

        try:
            limit = int(limit)
            if limit < 0:
                raise ValueError
        except ValueError:
            limit = 10

        if search_query:
            return (
                Instrument.objects
               .filter(
                    Q(company__translations__title__icontains=search_query) | Q(ticker__icontains=search_query),
                    company__is_visible=True,
                    instrument_type='share',
                )
                .select_related(
                    'company',
                    'exchange',
                    'currency',
                    'company__country',
                    'company__sector',
                    'company__industry',
                )
                .distinct()
                .order_by('ticker')
            )[:limit]

        return Instrument.objects.none()


class ShareDetailAPIView(RetrieveAPIView):
    serializer_class = serializers.ShareFullSerializer
    multiple_lookup_fields = {
        'exchange__slug': 'exchange',
        'ticker': 'ticker'
    } # {'URL lookup:lookup Field'}

    def get_object(self):
        queryset = self.get_queryset()
        filters = {
            key: self.kwargs[field].upper()
            for key, field in self.multiple_lookup_fields.items()
        }

        obj = get_object_or_404(queryset, **filters)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return (
            Instrument.objects
            .filter(company__is_visible=True)
            .select_related(
                'company',
                'exchange',
                'currency',
                'company__country',
                'company__sector',
                'company__industry',
            )
        )


class ShareDetailCandleListAPIView(ListAPIView):
    serializer_class = serializers.CandleSerializer

    def get_queryset(self):
        exchange = self.kwargs.get('exchange', '')
        ticker = self.kwargs.get('ticker', '')

        try:
            instrument = Instrument.objects.get(
                exchange__slug=exchange.upper(),
                ticker=ticker.upper(),
                company__is_visible=True,
                instrument_type='share',
            )
        except Instrument.DoesNotExist:
            raise exceptions.NotFound(f'Share ({exchange}-{ticker}) does not exist',)

        return instrument.candles.all()
