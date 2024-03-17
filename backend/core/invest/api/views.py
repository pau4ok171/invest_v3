from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from invest.api.serializers import CompanySerializer, CandlePerDaySerializer
from invest.models import Company, CandlePerDay

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
            serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"companies": []})


