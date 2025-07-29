from rest_framework import serializers

from apps.invest.models import Company

from .models import Portfolio


class PortfoliosSerializer(serializers.ModelSerializer):
    positions = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Company.objects.filter(is_visible=True),
        required=False
    )

    class Meta:
        model = Portfolio
        fields = (
            'id',
            'name',
            'created',
            'updated',
            'positions',
        )
        extra_kwargs = {
            'id': { 'read_only': True },
            'created': { 'read_only': True },
            'updated': { 'read_only': True },
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        positions_data = validated_data.pop('positions', [])

        portfolio = Portfolio.objects.create(**validated_data, user=user)

        profile = user.profile
        profile.portfolios.add(portfolio)

        if positions_data:
            portfolio.positions.set(positions_data)

        return portfolio

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions', None)

        instance = super().update(instance, validated_data)

        if positions_data is not None:
            instance.positions.set(positions_data)

        return instance
