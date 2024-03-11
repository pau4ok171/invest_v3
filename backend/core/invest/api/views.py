from rest_framework.generics import ListAPIView

from invest.api.serializers import CompanySerializer, CandlePerDaySerializer
from invest.models import Company, CandlePerDay

from django.db.models import Q


class PriceChartList(ListAPIView):
    serializer_class = CandlePerDaySerializer

    def get_queryset(self):
        return CandlePerDay.objects.filter(company__slug__exact=self.kwargs.get('company_slug'))


class SearchList(ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        return Company.objects.filter(
            Q(title__icontains=query) | Q(ticker__icontains=query),
            is_visible=True
        )
