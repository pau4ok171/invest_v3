from rest_framework import serializers

from apps.invest import models
from apps.invest.serializers import CandleSerializer
from apps.invest.serializers.company.serializers import (
    CompanySerializer,
    CompanyFullSerializer,
)
from apps.invest.serializers.serializers import (
    ExchangeSerializer,
    CurrencySerializer,
    DividendSerializer,
)
from apps.invest.services.company import ShareService
from apps.notes.models import Note
from apps.notes.serializers import NoteSerializer


class BaseShareSerializer(serializers.ModelSerializer):
    absolute_url = serializers.CharField(source='get_absolute_url', read_only=True)
    company = CompanySerializer(read_only=True)
    exchange = ExchangeSerializer(read_only=True)
    currency = CurrencySerializer(read_only=True)
    last_candle = serializers.SerializerMethodField()

    class Meta:
        model = models.Instrument
        fields = [
            'ticker',
            'isin',
            'lot',
            'exchange',
            'currency',
            'last_candle',
            'absolute_url',
            'company',
        ]

    @staticmethod
    def get_last_candle(instance: models.Instrument):
        last_candle = instance.candles.order_by('-time').first()
        return CandleSerializer(last_candle if last_candle else {}).data


class ShareSerializer(BaseShareSerializer):
    pass


class ShareFullSerializer(BaseShareSerializer):
    dividends = DividendSerializer(read_only=True, many=True)
    company = CompanyFullSerializer(read_only=True)
    notes = serializers.SerializerMethodField()
    peers = serializers.SerializerMethodField()

    class Meta(BaseShareSerializer.Meta):
        fields = BaseShareSerializer.Meta.fields + [
            'notes',
            'peers',
            'dividends',
        ]

    def get_notes(self, instance: models.Instrument):
        notes = {}
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            notes = Note.objects.filter(user=request.user, instrument=instance)
        return NoteSerializer(notes, many=True).data

    @staticmethod
    def get_peers(instance: models.Instrument):
        peers = ShareService.get_peers(instance)
        return ShareSerializer(peers, many=True).data