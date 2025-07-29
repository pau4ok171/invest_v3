from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Portfolio
from .permissions import IsPortfolioOwner
from .serializers import PortfoliosSerializer


class PortfoliosViewSet(ModelViewSet):
    serializer_class = PortfoliosSerializer
    permission_classes = [permissions.IsAuthenticated, IsPortfolioOwner]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)
