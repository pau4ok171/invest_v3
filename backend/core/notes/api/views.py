from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from invest.models import Company
from .serializers import NoteSerializer
from notes.models import Note


class NotesViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        note = Note.objects.create(
            company=Company.objects.get(pk=self.request.data.get('company_id')),
            user=self.request.user,
            body=self.request.data.get('content'),
        )
        serializer = NoteSerializer(note)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        Note.objects\
            .filter(pk=self.request.data.get('note_id'))\
            .update(body=self.request.data.get('content'), updated=self.request.data.get('updated'))

        serializer = self.serializer_class(Note.objects.get(pk=self.kwargs.get('pk')))
        return Response(serializer.data)
