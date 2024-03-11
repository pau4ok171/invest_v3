from rest_framework.serializers import ModelSerializer
from portfolio.models import Portfolio


class PortfolioPositionsSerializer(ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'
        depth = 1


class PortfolioSerializer(ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'
