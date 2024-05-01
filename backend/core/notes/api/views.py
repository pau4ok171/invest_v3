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
        company_id = self.request.data.get('company_id', None)
        body = self.request.data.get('content', None)

        if not company_id:
            return Response({'error': 'Company ID was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not body:
            return Response({'error': 'Content was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        note = Note.objects.create(
            company=Company.objects.get(pk=company_id),
            user=self.request.user,
            body=body,
        )
        serializer = NoteSerializer(note)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        note_id = self.request.data.get('note_id', None)
        body = self.request.data.get('content', None)
        updated = self.request.data.get('updated', None)

        if not note_id:
            return Response({'error': 'Note ID was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not body:
            return Response({'error': 'Body was not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not updated:
            return Response({'error': 'Updated was not provided'}, status=status.HTTP_400_BAD_REQUEST)

        Note.objects.filter(pk=note_id).update(body=body, updated=updated)
        serializer = self.serializer_class(Note.objects.get(pk=note_id))
        return Response(serializer.data)
