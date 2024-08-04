from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .serializers import (
    CompaniesSerializer,
    CompanySerializer,
    CountrySerializer,
    MarketSerializer,
    SectorSerializer,
    IndustrySerializer
)
from invest.models import Company, Country, Market, Sector, Industry


class CompaniesListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CompaniesSerializer
    queryset = Company.objects.all()


class CompanyAPIView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CompanySerializer

    def get_object(self):
        company_uid = self.kwargs.get('company_uid')
        return Company.objects.get(uid=company_uid) if company_uid else None


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
