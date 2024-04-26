import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status, authentication, permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


from invest.api.serializers import CompanySerializer, CandlePerDaySerializer, SorterSerializer, CountrySerializer, SectorSerializer, CompanySearchSerializer, CompanyDetailSerializer
from invest.api.paginators import StandardResultsSetPagination
from invest.models import Company, CandlePerDay, Sorter, Country, Sector, AnalystIdea

from portfolio.models import Portfolio
from portfolio.api.serializers import PortfolioSerializer

from notes.models import Note
from notes.api.serializers import NoteSerializer

from django.db.models import Q


class PriceChartList(ListAPIView):
    serializer_class = CandlePerDaySerializer

    def get_queryset(self):
        return CandlePerDay.objects.filter(company__slug__exact=self.kwargs.get('company_slug'))


class SearchList(APIView):
    def post(self, request):
        query = request.data.get('query', None)
        if query:
            companies = Company.objects.filter(
                Q(title__icontains=query) | Q(ticker__icontains=query),
                is_visible=True
            )
            serializer = CompanySearchSerializer(companies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"companies": []})


@api_view(['POST'])
def validate_username(request):
    username = request.data.get('username', None)
    is_taken = User.objects.filter(username__iexact=username).exists()
    message = "The username is already taken" if is_taken else "The username is free"

    return Response({
        "isTaken": is_taken,
        "message": message
    })


class CompanyListView(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = StandardResultsSetPagination
    serializer_class = CompanySerializer

    def get_queryset(self):
        country_slug = self.kwargs.get('country_slug', 'global')
        sector_slug = self.kwargs.get('sector_slug', 'any')

        queryset = Company.objects.filter(is_visible=True)

        if not country_slug == 'global':
            queryset = queryset.filter(country__name_iso=country_slug)
        if not sector_slug == 'any':
            queryset = queryset.filter(sector__slug=sector_slug)

        return queryset


class CompanyListFilters(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def __init__(self):
        super().__init__()
        self.companies = None

    def get(self, request, *args, **kwargs):
        self.companies = Company.objects.filter(is_visible=True)
        return Response({
            'filters': {
                'sorter': self.get_sorter_data(),
                'country': self.get_country_data(),
                'sector': self.get_sector_data(),
            },
            'list_updated': self.get_list_updated(),
        })

    def get_sector_data(self):
        sectors = Sector.objects.filter(company__pk__in=self.companies).distinct()
        sector_serializer = SectorSerializer(sectors, many=True)
        return sector_serializer.data

    def get_country_data(self):
        countries = Country.objects.filter(company__pk__in=self.companies).distinct()
        country_serializer = CountrySerializer(countries, many=True)
        return country_serializer.data

    @staticmethod
    def get_sorter_data():
        sorters = Sorter.objects.all()
        sorter_serializer = SorterSerializer(sorters, many=True)
        return sorter_serializer.data

    def get_list_updated(self):
        return self.companies.values_list('updated').latest('updated')[0].strftime('%d %b, %Y')


class CompanyListSectorFilters(CompanyListFilters):
    def get(self, request, *args, **kwargs):
        country_slug = self.kwargs.get('country_slug', 'global')
        self.companies = Company.objects.filter(is_visible=True)
        if not country_slug == 'global':
            self.companies = self.companies.filter(country__name_iso=country_slug)
        return Response({
            'filters': {
                'sector': self.get_sector_data(),
            },
        })


class WatchlistedCompanyAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        company_uid = request.data.get('uid')
        company = Company.objects.get(uid=company_uid)
        company.users_watchlist.add(self.request.user)
        return JsonResponse(
            data={
                "status": 201
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        company_uid = request.data.get('uid')
        company = Company.objects.get(uid=company_uid)
        company.users_watchlist.remove(self.request.user)
        return JsonResponse(
            data={
                "status": 204
            },
            status=status.HTTP_204_NO_CONTENT
        )


class CompanyDetailAPIView(RetrieveAPIView):
    queryset = Company.objects.filter(is_visible=True)
    serializer_class = CompanyDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = 'slug'
    lookup_url_kwarg = 'company_slug'

    def retrieve(self, request, *args, **kwargs):
        company_instance = self.get_object()
        company_serializer = self.get_serializer(company_instance)
        portfolio_serializer = self._get_portfolio_serializer()
        note_serializer = self._get_note_serializer()

        return Response({
            "company": company_serializer.data,
            "portfolios": portfolio_serializer.data,
            "notes": note_serializer.data,
        })

    def _get_portfolio_serializer(self) -> PortfolioSerializer:
        if self.request.user.is_authenticated:
            portfolios = Portfolio.objects.filter(user=self.request.user)
        else:
            portfolios = {}
        return PortfolioSerializer(portfolios, many=True)

    def _get_note_serializer(self) -> NoteSerializer:
        if self.request.user.is_authenticated:
            notes = Note.objects.filter(user=self.request.user, company=self.get_object())
        else:
            notes = {}
        return NoteSerializer(notes, many=True)
