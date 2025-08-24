from django.db.models import Count

from rest_framework import serializers

from parler_rest.serializers import TranslatedFieldsField

from apps.invest import models
from apps.invest.serializers.serializers import (
    CountrySerializer,
    SectorSerializer,
    AnalystIdeaSerializer,
)

from apps.statements.models import Statement
from apps.statements.serializers import StatementSerializer
from apps.statements.types import Status
from apps.news.serializers import NewsSerializer


class BaseCompanySerializer(serializers.ModelSerializer):
    translations = TranslatedFieldsField(shared_model=models.Company)
    country = CountrySerializer(read_only=True)
    sector = SectorSerializer(read_only=True)
    logo_url = serializers.CharField(source='get_logo', read_only=True)
    snowflake = serializers.SerializerMethodField()

    class Meta:
        model = models.Company
        fields = [
            'uid',
            'logo_url',
            'country',
            'sector',
            'snowflake',
            'translations',
        ]

    @staticmethod
    def get_snowflake(instance: models.Company):
        area_map = {
            'VALUE': 'value',
            'FUTURE': 'future',
            'PAST': 'past',
            'HEALTH': 'health',
            'DIVIDENDS': 'dividends',
        }

        counts = Statement.objects.filter(
            company=instance,
            area__in=area_map.keys(),
            status=Status.PASS,
            outcome=1002
        ).values('area').annotate(count=Count('id'))

        snowflake = {area: 0 for area in area_map.values()}

        for item in counts:
            snowflake[area_map[item['area']]] = item['count']

        return snowflake


class CompanySerializer(BaseCompanySerializer):
    pass


class CompanyPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyPerformance
        fields = (
            'return_7d',
            'return_30d',
            'return_90d',
            'return_1y',
            'return_3y',
            'return_5y',
            'average_weekly_movement',
            'last_reported_earnings',
            'next_earnings',
        )


class CompanyFullSerializer(CompanySerializer):
    analyst_ideas = AnalystIdeaSerializer(source='analyst_idea', many=True)
    company_news = NewsSerializer(read_only=True, many=True)
    performance = CompanyPerformanceSerializer(read_only=True)
    statements = StatementSerializer(read_only=True, many=True)

    class Meta(BaseCompanySerializer.Meta):
        fields = BaseCompanySerializer.Meta.fields + [
            'analyst_ideas',
            'company_news',
            'performance',
            'year_founded',
            'website',
            'statements',
        ]
