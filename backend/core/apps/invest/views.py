# Django
from django.contrib.auth.models import User
from django.db.models import Q
# DRF
from rest_framework import status, exceptions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Invest App
from .serializers import (
    CompanySerializer,
    CandlePerDaySerializer,
    CountrySerializer,
    SectorFilterSerializer,
    CompanySearchSerializer,
    CompanyDetailSerializer,
    CompanyPeersSerializer,
    CurrencySerializer,
)
from .services.company import CompanyService
from .paginators import StandardResultsSetPagination
from .models import Company, Country, Sector, Currency
from .forms import (
    SearchListForm,
    UsernameVerificationForm,
)
# Notes App
from apps.notes.models import Note
from apps.notes.serializers import NoteSerializer
from apps.statements.serializers import StatementSerializer
from apps.statements.models import Statement


@api_view(['GET'])
def validate_username(request):
    form = UsernameVerificationForm(request.query_params)
    if form.is_valid():
        username = form.cleaned_data['username']
        is_taken = User.objects.filter(username__iexact=username).exists()
        message = "The username is already taken" if is_taken else "The username is free"
        return Response(data={
            "isTaken": is_taken,
            "message": message
        }, status=status.HTTP_200_OK)
    return Response(data={"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_query(request):
    form = SearchListForm(data=request.query_params)
    if form.is_valid():
        query = form.cleaned_data['query']
        companies = Company.objects.filter(
            Q(translations__title__icontains=query) | Q(ticker__icontains=query),
            is_visible=True
        )
        return Response(
            data=CompanySearchSerializer(companies, many=True).data,
            status=status.HTTP_200_OK
        )
    return Response(data={"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class PriceChartList(ListAPIView):
    serializer_class = CandlePerDaySerializer

    def get_queryset(self):
        try:
            company = Company.objects.get(slug=self.kwargs.get('company_slug'))
        except Company.DoesNotExist:
            raise exceptions.NotFound(
                detail=f'Company with slug \'{self.kwargs.get("company_slug")}\' does not exist',
            )
        return company.candle.all()


class CompanyListView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = CompanySerializer

    def get_queryset(self):
        country_slug = self.request.query_params.get('country', 'global')
        sector_slug = self.request.query_params.get('sector', 'any')

        queryset = Company.objects.filter(
            is_visible=True
        ).select_related(
            'country',
            'market',
            'sector'
        ).distinct()

        if not country_slug == 'global':
            queryset = queryset.filter(country__iso_code=country_slug)
        if not sector_slug == 'any':
            queryset = queryset.filter(sector__slug=sector_slug)

        return queryset


class CompanyListCountries(ListAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        country_ids = Country.objects.filter(
            company__is_visible=True
        ).distinct().values_list('id', flat=True)

        return (
            Country.objects
            .filter(id__in=country_ids)
            .prefetch_related(
                'translations',
                'currency',
                'market'
            )
            .order_by('iso_code')
        )

class CountryOptions(ListAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        return (
            Country.objects
            .all()
            .prefetch_related(
                'translations',
                'currency',
                'market'
            )
            .order_by('iso_code')
        )


class CurrencyOptions(ListAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


class CompanyListSectors(ListAPIView):
    serializer_class = SectorFilterSerializer

    def get_queryset(self):
        sector_ids = Sector.objects.filter(
            company__is_visible=True
        ).distinct().values_list('id', flat=True)

        return (
            Sector.objects
            .filter(id__in=sector_ids)
            .prefetch_related(
                'translations',
            )
            .order_by('slug')
        )


class CompanyDetailAPIView(RetrieveAPIView):
    queryset = Company.objects.filter(is_visible=True).select_related(
        'country', 'market', 'sector', 'country__currency'
    ).prefetch_related('report', 'analyst_idea', 'company_news', 'dividend')
    serializer_class = CompanyDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'company_slug'

    def retrieve(self, request, *args, **kwargs):
        return Response({
            "company": self.get_company_serializer().data,
            "notes": self.get_note_serializer().data,
            "statements": self.get_statement_serializer().data,
            "peers": self.get_peers_serializer().data,
        })

    def get_company_serializer(self):
        return self.get_serializer(self.get_object())

    def get_note_serializer(self) -> NoteSerializer:
        notes = {}
        if self.request.user.is_authenticated:
            notes = Note.objects.filter(user=self.request.user, company=self.get_object())
        return NoteSerializer(notes, many=True)

    def get_statement_serializer(self):
        statements = Statement.objects.filter(company=self.get_object())
        return StatementSerializer(statements, many=True)


    def get_peers_serializer(self):
        peers = CompanyService.get_peers(self.get_object())
        return CompanyPeersSerializer(peers, many=True)
