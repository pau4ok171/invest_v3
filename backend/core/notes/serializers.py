from rest_framework.serializers import ModelSerializer

from notes.models import Note


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'company', 'body', 'text', 'created_at', 'updated_at')
