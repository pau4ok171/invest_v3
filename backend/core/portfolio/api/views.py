from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework import status
from django.http import JsonResponse
from portfolio.models import Portfolio, PortfolioCompany
from invest.models import Company
from .serializers import PortfolioPositionsSerializer, PortfolioSerializer


class PortfolioPositionsAPI(RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioPositionsSerializer

    def patch(self, request, *args, **kwargs):
        portfolio_id = self.request.POST.get('portfolio_id')
        _portfolio = Portfolio.objects.get(pk__iexact=portfolio_id)

        company_slug = self.request.POST.get('company_slug')
        company = Company.objects.get(slug__iexact=company_slug)

        PortfolioCompany.objects.create(company=company, portfolio=_portfolio)

        total_positions = Portfolio.objects.get(pk__exact=portfolio_id).positions.count()

        return JsonResponse(
            data={
                'status': 201,
                'total_positions': total_positions
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        portfolio_id = self.request.POST.get('portfolio_id')
        company_slug = self.request.POST.get('company_slug')

        portfolio_company = PortfolioCompany.objects.get(
            company__slug__iexact=company_slug,
            portfolio_id__exact=portfolio_id,
        )
        portfolio_company.delete()

        total_positions = Portfolio.objects.get(pk__exact=portfolio_id).positions.count()

        return JsonResponse(
            data={
                'total_positions': total_positions,
                'status': 204
            },
            status=status.HTTP_200_OK
        )


class CreatePortfolioAPI(CreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        name = self.request.POST.get('name')
        portfolio = Portfolio.objects.create(user=user, name=name)
        portfolio_serialized = PortfolioSerializer(portfolio)
        return JsonResponse(
            data=portfolio_serialized.data,
            status=status.HTTP_201_CREATED
        )




