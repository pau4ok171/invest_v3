import os.path
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from invest.models import Company, Country, Industry, Market, Sector, Currency

URL_PREFIX = settings.URL_PREFIX


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = (
            'name',
            'symbol',
        )


class CountrySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    flag_url = serializers.CharField(source='get_flag_url', read_only=True)

    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'name_iso',
            'currency',
            'flag_url',
        )


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = (
            'title',
            'slug',
            'sector',
        )


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = (
            'title',
            'slug',
            'country',
        )


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = (
            'id',
            'title',
            'slug',
        )


class UserSerializer(serializers.ModelSerializer):
    stage_in_days = serializers.SerializerMethodField(source='get_stage_in_days', read_only=True)
    is_staff = serializers.SerializerMethodField(source='get_is_staff', read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'is_staff',
            'is_anonymous',
            'stage_in_days',
        )

    @staticmethod
    def get_stage_in_days(obj) -> int:
        now = datetime.datetime.now(tz=datetime.UTC)
        return (now - obj.date_joined).days

    @staticmethod
    def get_is_staff(obj):
        return obj.is_staff


class CompaniesSerializer(serializers.ModelSerializer):
    market_name = serializers.SerializerMethodField('get_market_name')
    sector_name = serializers.SerializerMethodField('get_sector_name')
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Company
        fields = (
            'id',
            'ticker',
            'slug',
            'uid',
            'title',
            'short_title',
            'is_visible',
            'logo',
            'is_fund',
            'market_name',
            'sector_name',
            'absolute_url',
        )

    @staticmethod
    def get_market_name(instance):
        return instance.market.title

    @staticmethod
    def get_sector_name(instance):
        return instance.sector.title


class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(
        allow_null=True,
        default=os.path.join(settings.MEDIA_ROOT, 'companies/logos/default.png')
    )

    class Meta:
        model = Company
        fields = (
            'ticker',
            'slug',
            'uid',
            'title',
            'short_title',
            'short_title_genitive',
            'description',
            'short_description',
            'city',
            'country',
            'market',
            'sector',
            'industry',
            'created',
            'updated',
            'created_by',
            'updated_by',
            'is_visible',
            'logo',
            'is_fund',
            'website',
            'year_founded',
        )

    @staticmethod
    def validate_year_founded(value):
        current_year = timezone.now().year
        if value > current_year or value < 1000:
            raise serializers.ValidationError('Must be a valid Year')
        return value

    @staticmethod
    def validate_logo(value: InMemoryUploadedFile | str | None):
        if not isinstance(value, InMemoryUploadedFile):
            return value

        if value.size > 100 * 1024:
            serializers.ValidationError('The image must be max 100Kb')
        return value

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['country'] = CountrySerializer(instance.country).data
        response['logo'] = instance.get_logo()
        response['industry'] = IndustrySerializer(instance.industry).data
        response['market'] = MarketSerializer(instance.market).data
        response['sector'] = SectorSerializer(instance.sector).data
        response['created_by'] = UserSerializer(instance.created_by).data
        response['updated_by'] = UserSerializer(instance.updated_by).data
        return response

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates, we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            elif attr == 'logo' and value is None:
                img_path = os.path.join(settings.MEDIA_ROOT, 'companies/logos/default.png')
                setattr(instance, attr, img_path)
            else:
                setattr(instance, attr, value)

        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance, and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance
