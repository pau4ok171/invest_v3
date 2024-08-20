import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .serializers import (
    CompaniesSerializer,
    CompanySerializer,
    CountrySerializer,
    MarketSerializer,
    SectorSerializer,
    IndustrySerializer,
)
from invest.models import Company, Country, Market, Sector, Industry


class CompaniesListAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CompaniesSerializer
    queryset = Company.objects.all()

    def create(self, request, *args, **kwargs):
        # Prepare Data
        data = get_data(request)

        # Create Serializer
        serializer = CompanySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CompanyAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CompanySerializer

    def get_object(self):
        company_uid = self.kwargs.get('company_uid')
        return Company.objects.get(uid=company_uid) if company_uid else None

    def update(self, request, *args, **kwargs):
        data = get_data(request)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class SelectorOptionsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request, *args, **kwargs):
        # Get countries list
        countries = Country.objects.all()
        countries_serializer = CountrySerializer(countries, many=True)
        # Get markets list
        markets = Market.objects.all()
        markets_serializer = MarketSerializer(markets, many=True)
        # Get sectors list
        sectors = Sector.objects.all()
        sectors_serializer = SectorSerializer(sectors, many=True)
        # Get industries list
        industries = Industry.objects.all()
        industries_serializer = IndustrySerializer(industries, many=True)

        return Response(
            data={
                'countries': countries_serializer.data,
                'markets': markets_serializer.data,
                'sectors': sectors_serializer.data,
                'industries': industries_serializer.data,
            },
            status=status.HTTP_200_OK
        )


def get_data(request):
    data = {key: val for key, val in request.data.items() if val}

    if data.get('country_name_iso'):
        data['country'] = Country.objects.get(name_iso=data.pop('country_name_iso')).pk
    if data.get('market_slug'):
        data['market'] = Market.objects.get(slug=data.pop('market_slug')).pk
    if data.get('sector_slug'):
        data['sector'] = Sector.objects.get(slug=data.pop('sector_slug')).pk
    if data.get('industry_slug'):
        data['industry'] = Industry.objects.get(slug=data.pop('industry_slug')).pk
    if type(data.get('logo')) == str and type(data.get('logo')) is not None:
        data.pop('logo')

    data['created_by'] = request.user.pk
    data['updated_by'] = request.user.pk
    data['created'] = datetime.datetime.utcnow()
    data['updated'] = datetime.datetime.utcnow()

    return data
