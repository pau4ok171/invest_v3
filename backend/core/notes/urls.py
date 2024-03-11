from django.urls import path, include

app_name = 'notes'

urlpatterns = [
    path('api/v1/', include('notes.api.urls', namespace='notes_api')),
]
