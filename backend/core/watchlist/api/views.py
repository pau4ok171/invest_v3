from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status

from invest.models import Company

from .serializers import WatchlistUserSerializer

# TODO: SUPPRIMER AU MOMENT VENU


class CreateWatchlistedCompany(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = WatchlistUserSerializer

    def patch(self, request, *args, **kwargs):
        company = self.get_company()
        if not company:
            return Response(data={"error": "Company Slug was not provided"}, status=status.HTTP_400_BAD_REQUEST)

        company.users_watchlist.add(self.request.user)

        return Response(
            data={
                "status": 201
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        company = self.get_company()
        if not company:
            return Response(data={"error": "Company Slug was not provided"}, status=status.HTTP_400_BAD_REQUEST)

        company.users_watchlist.remove(self.request.user)
        return Response(
            data={
                "status": 204
            },
            status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, *args, **kwargs):
        company = self.get_company()
        if not company:
            return Response(data={"error": "Company Slug was not provided"}, status=status.HTTP_400_BAD_REQUEST)

        is_company_in_watchlist = self.request.user in company.users_watchlist

        return Response(
            data={
                "is_company_in_watchlist": is_company_in_watchlist,
                "status": 200
            },
            status=status.HTTP_200_OK
        )

    def get_company(self):
        company_slug = self.request.POST.get('slug', None)

        if company_slug:
            return Company.objects.get(slug__iexact=company_slug)
