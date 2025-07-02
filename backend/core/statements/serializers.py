from rest_framework.serializers import ModelSerializer
from statements.models import Statement


class StatementSerializer(ModelSerializer):
    class Meta:
        model = Statement
        fields = '__all__'
