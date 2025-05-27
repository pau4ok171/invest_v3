from rest_framework import serializers
from django.contrib.auth.models import User


class TimestampField(serializers.Field):
    """Сериализатор для преобразования даты в timestamp"""

    def to_representation(self, value):
        return int(value.timestamp() * 1000) if value else None


class UserProfileSerializer(serializers.ModelSerializer):
    # Основные поля из User
    name = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source='profile.avatar', required=False)
    locale = serializers.CharField(source='profile.locale', required=False)
    register_date = TimestampField(source='date_joined', read_only=True)
    country_iso = serializers.CharField(source='profile.country_iso', required=False)
    currency = serializers.CharField(source='profile.currency', required=False)
    auth_provider = serializers.CharField(source='profile.auth_provider', read_only=True)
    display_name = serializers.CharField(source='profile.display_name', required=False)
    stock_view = serializers.CharField(source='profile.stock_view', required=False)

    # Вложенные структуры
    portfolios = serializers.SerializerMethodField()
    watchlist = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'first_name', 'last_name',
            'avatar', 'locale', 'register_date', 'country_iso',
            'currency', 'auth_provider', 'display_name',
            'portfolios', 'watchlist', 'stock_view', 'is_staff',
        ]
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})

        instance = super().update(instance, validated_data)

        # Обновление Profile
        if hasattr(instance, 'profile'):
            profile = instance.profile
            for attr, value in profile_data.items():
                # Обработка вложенных полей
                if attr == 'country_iso':
                    profile.country_iso = value['iso'] if isinstance(value, dict) else value
                elif attr == 'currency':
                    profile.currency = value['code'] if isinstance(value, dict) else value
                else:
                    setattr(profile, attr, value)
            profile.save()

        return instance

    @staticmethod
    def get_name(obj):
        """Формируем поле name из first_name и last_name"""
        return f"{obj.first_name} {obj.last_name}" if obj.first_name or obj.last_name else obj.username

    @staticmethod
    def get_portfolios(obj):
        """Список портфелей в упрощенном формате"""
        if hasattr(obj, 'profile'):
            return list(obj.profile.portfolios.values_list('id', flat=True))
        return []

    @staticmethod
    def get_watchlist(obj):
        """Список компаний в watchlist"""
        if hasattr(obj, 'profile'):
            return list(obj.profile.watchlist_companies.values_list('id', flat=True))
        return []

    def validate(self, attrs):
        protected_fields = ['id', 'register_date', 'auth_provider', 'is_staff']
        for field in protected_fields:
            if field in attrs and getattr(self.instance, field) != attrs[field]:
                raise serializers.ValidationError(
                    {field: f'Cannot update {field} field'}
                )
        return attrs
