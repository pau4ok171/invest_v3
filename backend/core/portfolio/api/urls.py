from django.urls import path
from .views import PortfolioPositionsAPI, CreatePortfolioAPI

app_name = 'portfolio_api'

urlpatterns = [
    path('create_portfolio/', CreatePortfolioAPI.as_view()),
    path('portfolio_positions/', PortfolioPositionsAPI.as_view()),
]
