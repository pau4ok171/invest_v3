from rest_framework import serializers

from apps.notes.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = (
            'id',
            'instrument',
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
        if 'instrument' in validated_data:
            raise serializers.ValidationError(
                {"instrument": "You cannot change the instrument after creation."}
            )
        return super().update(instance, validated_data)