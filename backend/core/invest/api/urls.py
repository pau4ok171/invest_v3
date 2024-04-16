from django.urls import path
from invest.api import views

app_name = 'invest_api'

urlpatterns = [
    path('companies/', views.CompanyListView.as_view()),
    path('companies/<slug:country_slug>/<slug:sector_slug>', views.CompanyListView.as_view()),
    path('company/<slug:company_slug>', views.CompanyDetailAPIView.as_view()),
    path('filters/', views.CompanyListFilters.as_view()),
    path('filters/sector/<slug:country_slug>', views.CompanyListSectorFilters.as_view()),
    path('toggle_to_watchlist/', views.WatchlistedCompanyAPIView.as_view()),
    path('search/', views.SearchList.as_view()),
    path('validate_username/', views.validate_username),
    path('price_chart/<slug:company_slug>/', views.PriceChartList.as_view(), name='price_chart'),
    path('price_chart_new/<slug:company_slug>/', views.PriceChartList.as_view(), name='price_chart_new'),
]
