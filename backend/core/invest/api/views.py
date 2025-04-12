# Django
from django.contrib.auth.models import User
from django.db.models import Q
# DRF
from rest_framework import status, authentication
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# Invest App
from invest.api.serializers import (
    CompanySerializer,
    CandlePerDaySerializer,
    CountrySerializer,
    SectorSerializer,
    CompanySearchSerializer,
    CompanyDetailSerializer,
    CompanyPeersSerializer
)
from invest.api.paginators import StandardResultsSetPagination
from invest.models import Company, CandlePerDay, Country, Sector
from invest.api.forms import (
    SearchListForm,
    UsernameVerificationForm,
    CompanyUIDForm,
)
# Portfolio App
from portfolio.models import Portfolio
from portfolio.api.serializers import PortfolioSerializer
# Notes App
from notes.models import Note
from notes.api.serializers import NoteSerializer
from statements.api.serializers import StatementSerializer
from statements.models import Statement
from statements.types import Status, Area


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
            Q(title__icontains=query) | Q(ticker__icontains=query),
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
        return CandlePerDay.objects.filter(company__slug__exact=self.kwargs.get('company_slug'))


class CompanyListView(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    pagination_class = StandardResultsSetPagination
    serializer_class = CompanySerializer

    def get_queryset(self):
        country_slug = self.request.query_params.get('country', 'global')
        sector_slug = self.request.query_params.get('sector', 'any')

        queryset = Company.objects.filter(is_visible=True)

        if not country_slug == 'global':
            queryset = queryset.filter(country__name_iso=country_slug)
        if not sector_slug == 'any':
            queryset = queryset.filter(sector__slug=sector_slug)

        return queryset


class CompanyListCountries(ListAPIView):
    serializer_class = CountrySerializer

    def get_queryset(self):
        companies = Company.objects.filter(is_visible=True)
        return Country.objects.filter(company__pk__in=companies).distinct()


class CompanyListSectors(ListAPIView):
    serializer_class = SectorSerializer

    def get_queryset(self):
        companies = Company.objects.filter(is_visible=True)
        return Sector.objects.filter(company__pk__in=companies).distinct()


class WatchlistedCompanyAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        form = CompanyUIDForm(self.request.data)
        if form.is_valid():
            company = Company.objects.get(uid=form.cleaned_data['uid'])
            company.users_watchlist.add(self.request.user)
            return Response(
                data={
                    "status": 201
                },
                status=status.HTTP_201_CREATED
            )
        return Response(data={"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        form = CompanyUIDForm(self.request.data)
        if form.is_valid():
            company = Company.objects.get(uid=form.cleaned_data['uid'])
            company.users_watchlist.remove(self.request.user)
            return Response(data={"status": 204}, status=status.HTTP_204_NO_CONTENT)
        return Response(data={"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailAPIView(RetrieveAPIView):
    queryset = Company.objects.filter(is_visible=True)
    serializer_class = CompanyDetailSerializer
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = 'slug'
    lookup_url_kwarg = 'company_slug'

    def retrieve(self, request, *args, **kwargs):
        statements = Statement.objects.filter(company=self.get_object())
        return Response({
            "company": self.get_serializer(self.get_object()).data,
            "portfolios": self._get_portfolio_serializer().data,
            "notes": self._get_note_serializer().data,
            "statements": self._get_statement_serializer_data(),
            "snowflake": self._get_snowflake_serializer_data(statements),
            "peers": self._get_peers_serializer_data(),
        })

    def _get_portfolio_serializer(self) -> PortfolioSerializer:
        portfolios = {}
        if self.request.user.is_authenticated:
            portfolios = Portfolio.objects.filter(user=self.request.user)

        return PortfolioSerializer(portfolios, many=True)

    def _get_note_serializer(self) -> NoteSerializer:
        notes = {}
        if self.request.user.is_authenticated:
            notes = Note.objects.filter(user=self.request.user, company=self.get_object())

        return NoteSerializer(notes, many=True)

    def _get_statement_serializer_data(self):
        statements = Statement.objects.filter(company=self.get_object())
        serializer = StatementSerializer(statements, many=True)
        return serializer.data

    @staticmethod
    def _get_snowflake_serializer_data(statements):
        return {
            "value": statements.filter(area=Area.VALUE, status=Status.PASS).count(),
            "future": statements.filter(area=Area.FUTURE, status=Status.PASS).count(),
            "past": statements.filter(area=Area.PAST, status=Status.PASS).count(),
            "health": statements.filter(area=Area.HEALTH, status=Status.PASS).count(),
            "dividends": statements.filter(area=Area.DIVIDENDS, status=Status.PASS).count(),
        }

    def _get_peers_serializer_data(self):
        company_object = self.get_object()
        peers = Company.objects.filter(is_visible=True).exclude(pk=company_object.id)
        peers = sorted(peers, key=self._get_sort_key, reverse=True)[:4]
        serializer = CompanyPeersSerializer(peers, many=True)
        return serializer.data

    def _get_sort_key(self, iter_company):
        company_object = self.get_object()
        sector_id = company_object.sector.id
        country_id = company_object.country.id
        country_score = 4 if iter_company.country.id == country_id else 3
        sector_score = 4 if iter_company.sector.id == sector_id else 2
        return country_score + sector_score
