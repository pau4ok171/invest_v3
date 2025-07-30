from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.jwt_auth import JWTCookieAuthentication

from .serializers import NoteSerializer
from apps.notes.models import Note


class NotesViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTCookieAuthentication]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
