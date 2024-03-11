from django.urls import path, include

app_name = 'watchlist'

urlpatterns = [
    path('api/v1/', include('watchlist.api.urls', namespace='watchlist_api'))
]
