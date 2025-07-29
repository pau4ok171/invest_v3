from django.urls import path, include

from rest_framework.routers import SimpleRouter

from .views import PortfoliosViewSet

router = SimpleRouter()
router.register(r'', PortfoliosViewSet, basename='portfolios')

app_name = 'portfolio_api'

urlpatterns = [
    path('', include(router.urls)),
]
