from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.invest.models import Company

from .serializers import UserProfileSerializer
from .permissions import IsProfileOwner


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]
    http_method_names = ['get', 'put', 'patch', 'head', 'options']

    def get_queryset(self):
        return User.objects.select_related('profile').filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        protected_fields = ['id', 'register_date', 'auth_provider', 'is_staff']
        for field in protected_fields:
            if field in request.data:
                return Response(
                    {field: f'Updating {field} is not allowed'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['patch'])
    def update_watchlist(self, request):
        company_uid = request.data.get('company_uid')
        action_type = request.data.get('action')

        if not company_uid or action_type not in ['add', 'remove']:
            return Response(
                {"error": "Both 'action' and 'company_uid' are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            company = get_object_or_404(Company, uid=company_uid)
            profile = request.user.profile

            if action_type == 'add':
                profile.watchlisted_companies.add(company)
            else:
                profile.watchlisted_companies.remove(company)

            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
