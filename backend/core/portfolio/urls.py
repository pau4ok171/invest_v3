from django.urls import path, include

app_name = 'portfolio'

urlpatterns = [
    path('api/v1/', include('portfolio.api.urls', namespace='portfolio_api')),
]
