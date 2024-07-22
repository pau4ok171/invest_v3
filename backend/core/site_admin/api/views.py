from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .serializers import CompaniesSerializer
from invest.models import Company


class CompaniesListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = CompaniesSerializer
    queryset = Company.objects.all()
