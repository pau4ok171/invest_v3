from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import NotesViewSet

app_name = 'notes_api'

router = SimpleRouter()
router.register(r'notes', NotesViewSet, basename='notes')

urlpatterns = [
    path('', include(router.urls)),
]
