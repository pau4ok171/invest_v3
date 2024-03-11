from django.urls import path
from . import views

app_name = 'watchlist_api'

urlpatterns = [
    path('toggle_watchlisted_company/', views.CreateWatchlistedCompany.as_view(), name='toggle_watchlisted_company'),
]
