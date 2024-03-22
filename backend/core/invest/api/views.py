from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

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


@api_view(['POST'])
def validate_username(request):
    username = request.data.get('username', None)
    is_taken = User.objects.filter(username__iexact=username).exists()
    message = "The username is already taken" if is_taken else "The username is free"

    return Response({
        "isTaken": is_taken,
        "message": message
    })

