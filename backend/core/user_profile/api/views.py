from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserProfileSerializer
from ..permissions import IsProfileOwner


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']

    def get_queryset(self):
        return User.objects.select_related('profile').filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        protected_fields = ['id', 'register_date', 'auth_provider']
        for field in protected_fields:
            if field in request.data:
                return Response(
                    {field: f'Updating {field} is not allowed'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """Единый метод для GET и PATCH /me/"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        # Обработка PATCH
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
