from rest_framework import serializers
from invest.models import Company


class WatchlistUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['ticker', 'title', 'logo', 'country', 'market', 'sector', 'users_watchlist']
        depth = 1
