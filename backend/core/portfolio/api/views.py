from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

from portfolio.models import Portfolio, PortfolioCompany

from invest.models import Company

from .serializers import PortfolioPositionsSerializer, PortfolioSerializer


class PortfolioPositionsAPI(RetrieveUpdateDestroyAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioPositionsSerializer

    def patch(self, request, *args, **kwargs):
        portfolio_id = self.request.POST.get('portfolio_id', None)
        company_slug = self.request.POST.get('company_slug', None)

        if not portfolio_id:
            return Response({'error': 'Portfolio ID was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_slug:
            return Response({'error': 'Company Slug was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        portfolio = Portfolio.objects.get(pk__iexact=portfolio_id)
        company = Company.objects.get(slug__iexact=company_slug)

        PortfolioCompany.objects.create(company=company, portfolio=portfolio)

        total_positions = Portfolio.objects.get(pk__exact=portfolio_id).positions.count()

        return Response(
            data={
                "status": 201,
                "total_positions": total_positions
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        portfolio_id = self.request.POST.get('portfolio_id', None)
        company_slug = self.request.POST.get('company_slug', None)

        if not portfolio_id:
            return Response({'error': 'Portfolio ID was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_slug:
            return Response({'error': 'Company Slug was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        portfolio_company = PortfolioCompany.objects.get(
            company__slug__iexact=company_slug,
            portfolio_id__exact=portfolio_id,
        )
        portfolio_company.delete()

        total_positions = Portfolio.objects.get(pk__exact=portfolio_id).positions.count()

        return Response(
            data={
                "total_positions": total_positions,
                "status": 204
            },
            status=status.HTTP_200_OK
        )


class CreatePortfolioAPI(CreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        portfolio_name = self.request.POST.get('name', None)

        if not portfolio_name:
            return Response({'error': 'Portfolio Name was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        portfolio = Portfolio.objects.create(user=user, name=portfolio_name)
        portfolio_serialized = PortfolioSerializer(portfolio)
        return Response(
            data=portfolio_serialized.data,
            status=status.HTTP_201_CREATED
        )


class PortfoliosViewSet(ModelViewSet):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        portfolio_name = self.request.data.get('portfolio_name', None)

        if not portfolio_name:
            return Response({'error': 'Portfolio Name was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'name': portfolio_name,
            'user': self.request.user.pk
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        portfolio_id = self.kwargs.get('pk', None)
        company_id = self.request.data.get('company_id', None)
        action = self.request.data.get('action', None)

        if not portfolio_id:
            return Response({'error': 'Portfolio ID was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not company_id:
            return Response({'error': 'Company ID was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not action:
            return Response({'error': 'Action  was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        portfolio = Portfolio.objects.get(pk=portfolio_id)
        company = Company.objects.get(pk=company_id)

        if action == 'include':
            PortfolioCompany.objects.create(portfolio=portfolio, company=company)
        elif action == 'exclude':
            PortfolioCompany.objects.get(company=company, portfolio=portfolio).delete()

        serializer = self.serializer_class(portfolio)

        return Response(serializer.data)
