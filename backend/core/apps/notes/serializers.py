from rest_framework import serializers

from apps.notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'id',
            'company',
            'body',
            'text',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        return self.Meta.model.objects.create(**validated_data, user=request.user)

    def update(self, instance, validated_data):
        if 'company' in validated_data:
            raise serializers.ValidationError(
                {"company": "You cannot change the company after creation."}
            )
        return super().update(instance, validated_data)