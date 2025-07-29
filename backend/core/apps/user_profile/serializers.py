from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator

from rest_framework import serializers

from apps.invest.models import Country, Currency
from apps.portfolio.serializers import PortfoliosSerializer

from .models import THEME_CHOICES, STOCK_VIEW_CHOICES, Profile

hex_color_validator = RegexValidator(
    regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
    message='Enter a valid HEX color (e.g. #RRGGBB or #RGB)'
)

class TimestampField(serializers.Field):
    """Сериализатор для преобразования даты в timestamp"""

    def to_representation(self, value):
        return int(value.timestamp() * 1000) if value else None


class UserProfileSerializer(serializers.ModelSerializer):
    # Основные поля из User
    name = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source='profile.avatar', allow_null=True)
    locale = serializers.ChoiceField(source='profile.locale', choices=settings.LANGUAGES)
    country_iso = serializers.CharField(source='profile.country.iso_code')
    currency_iso = serializers.CharField(source='profile.currency.iso_code')
    display_name = serializers.CharField(source='profile.display_name')
    stock_view = serializers.ChoiceField(source='profile.stock_view', choices=STOCK_VIEW_CHOICES)
    registration_date = TimestampField(source='date_joined', read_only=True)
    auth_provider = serializers.CharField(source='profile.auth_provider', read_only=True)
    bio = serializers.CharField(source='profile.bio')
    external_link = serializers.URLField(source='profile.external_link')
    theme = serializers.ChoiceField(source='profile.theme', choices=THEME_CHOICES)
    banner_color = serializers.CharField(source='profile.banner_color', validators=[hex_color_validator])
    # Вложенные структуры
    portfolios = PortfoliosSerializer(source='profile.portfolios', many=True, read_only=True)
    watchlist = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            # User
            'id',
            'name',
            'first_name',
            'last_name',
            'email',
            'username',
            'is_staff',
            'registration_date',
            # Profile
            'display_name',
            'avatar',
            'locale',
            'country_iso',
            'currency_iso',
            'auth_provider',
            'bio',
            'external_link',
            'stock_view',
            'watchlist',
            'portfolios',
            'theme',
            'banner_color',
        )
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        profile, created = Profile.objects.get_or_create(user=instance)

        # Обновление Profile
        for key, value in profile_data.items():
            # Обработка вложенных полей
            if key == 'country' and 'iso_code' in value:
                profile.country = Country.objects.get(iso_code=value['iso_code'])
            elif key == 'currency' and 'iso_code' in value:
                profile.currency = Currency.objects.get(iso_code=value['iso_code'])
            else:
                setattr(profile, key, value)

        profile.save()

        instance = super().update(instance, validated_data)

        return instance

    @staticmethod
    def get_name(obj):
        """Формируем поле name из first_name и last_name"""
        return f"{obj.first_name} {obj.last_name}" if obj.first_name or obj.last_name else obj.username

    @staticmethod
    def get_watchlist(obj):
        """Список компаний в watchlist"""
        if hasattr(obj, 'profile'):
            return list(obj.profile.watchlisted_companies.values_list('uid', flat=True))
        return []

    @staticmethod
    def validate_country_iso(value):
        try:
            Country.objects.get(iso_code=value)
        except Country.DoesNotExist:
            raise serializers.ValidationError({
                'country_iso': f"Country with iso code: '{value}' does not exist"
            })
        return value

    @staticmethod
    def validate_currency_iso(value):
        try:
            Currency.objects.get(iso_code=value)
        except Currency.DoesNotExist:
            raise serializers.ValidationError({
                'currency_iso': f"Currency with iso code: '{value}' does not exist"
            })
        return value
