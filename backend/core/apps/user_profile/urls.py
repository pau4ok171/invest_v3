from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import UserProfileViewSet

app_name = 'profile_api'

router = SimpleRouter()
router.register(r'', UserProfileViewSet, basename='userprofile')

urlpatterns = [
    path('', include(router.urls)),
]
