from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from apps.invest.models import Company
from .serializers import NoteSerializer
from .forms import (
    NotesCreateForm,
    NotesUpdateForm,
)
from apps.notes.models import Note


class NotesViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        form = NotesCreateForm(self.request.data)
        if form.is_valid():
            company = Company.objects.get(pk=form.cleaned_data['company_id'])
            user = self.request.user
            body = form.cleaned_data['content']
            text = form.cleaned_data.get('text', '')

            note = Note.objects.create(company=company, user=user, body=body, text=text)
            serializer = NoteSerializer(note)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(data={"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        form = NotesUpdateForm(request.data)
        if form.is_valid():
            note_id = form.cleaned_data['note_id']
            body = form.cleaned_data['content']
            text = form.cleaned_data.get('text', '')
            updated_at = form.cleaned_data['updated_at']

            Note.objects.filter(pk=note_id).update(body=body, text=text, updated_at=updated_at)
            serializer = self.serializer_class(Note.objects.get(pk=note_id))
            return Response(serializer.data)
        return Response(data={"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        Note.objects.get(pk=kwargs.get('pk')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
