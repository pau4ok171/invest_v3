from django.urls import path
from . import views

app_name = 'invest_api'

urlpatterns = [
    # Objects
    path('companies/', views.CompanyListView.as_view()),
    path('companies/<slug:company_slug>/', views.CompanyDetailAPIView.as_view()),
    path('countries/', views.CompanyListCountries.as_view()),
    path('country-options/', views.CountryOptions.as_view()),
    path('currency-options/', views.CurrencyOptions.as_view()),
    path('sectors/', views.CompanyListSectors.as_view()),
    path('candles/<slug:company_slug>/', views.PriceChartList.as_view()),
    # Functions
    path('search-query/', views.search_query),
    path('validate-username/', views.validate_username),
]
