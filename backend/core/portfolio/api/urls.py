from django.urls import path, include
from .views import PortfoliosViewSet

from rest_framework import routers

app_name = 'portfolio_api'

router = routers.SimpleRouter()
router.register(r'portfolios', PortfoliosViewSet, basename='portfolios')

urlpatterns = [
    # Invest v3
    path('portfolios/', include(router.urls)),
]
