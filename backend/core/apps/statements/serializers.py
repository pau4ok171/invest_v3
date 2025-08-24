from rest_framework.serializers import ModelSerializer
from apps.statements.models import Statement


class StatementSerializer(ModelSerializer):
    class Meta:
        model = Statement
        fields = (
            'id',
            'name',
            'title',
            'description',
            'question',
            'level',
            'area',
            'type',
            'status',
            'severity',
            'outcome',
        )
