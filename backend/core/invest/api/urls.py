from django.urls import path
from invest.api import views

app_name = 'invest_api'

urlpatterns = [
    # Objects
    path('companies/', views.CompanyListView.as_view()),
    path('companies/<slug:company_slug>', views.CompanyDetailAPIView.as_view()),
    path('filters/', views.CompanyListFilters.as_view()),
    path('filters/sector/<country_slug>', views.CompanyListSectorFilters.as_view()),
    path('price_data/<slug:company_slug>/', views.PriceChartList.as_view()),
    path('toggle_to_watchlist/', views.WatchlistedCompanyAPIView.as_view()),
    # Functions
    path('search_query/', views.search_query),
    path('validate_username/', views.validate_username),
]
