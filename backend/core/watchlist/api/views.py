from invest.models import Company
from .serializers import WatchlistUserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status
from django.http import JsonResponse


class CreateWatchlistedCompany(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = WatchlistUserSerializer

    def patch(self, request, *args, **kwargs):
        company_slug = self.request.POST.get('slug')
        company = Company.objects.get(slug__iexact=company_slug)
        company.users_watchlist.add(self.request.user)
        return JsonResponse(
            data={
                "status": 201
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        company_slug = self.request.POST.get('slug')
        company = Company.objects.get(slug__iexact=company_slug)
        company.users_watchlist.remove(self.request.user)
        return JsonResponse(
            data={
                "status": 204
            },
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, *args, **kwargs):
        company_slug = self.request.POST.get('slug')
        company = Company.objects.get(slug__iexact=company_slug)
        is_company_in_watchlist = self.request.user in company.users_watchlist
        return JsonResponse(
            data={
                "is_company_in_watchlist": is_company_in_watchlist,
                "status": 200
            },
            status=status.HTTP_200_OK
        )
