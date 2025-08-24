from django.urls import path

from .views import views

app_name = 'invest_api'

urlpatterns = [
    # Companies
    path('companies/', views.CompanyListAPIView.as_view()),
    path('companies/<str:uid>/', views.CompanyDetailAPIView.as_view()),

    # Countries
    path('countries/', views.CountryListAPIView.as_view()),

    # Currencies
    path('currencies/', views.CurrencyListAPIView.as_view()),

    # Shares
    path('shares/', views.ShareListAPIView.as_view()),
    path('shares/countries/', views.ShareListCountryListAPIView.as_view()),
    path('shares/sectors/', views.ShareListSectorListAPIView.as_view()),
    path('shares/search/', views.ShareListSearchListAPIView.as_view()),
    path('shares/<str:exchange>-<str:ticker>/', views.ShareDetailAPIView.as_view()),
    path('shares/<str:exchange>-<str:ticker>/candles/', views.ShareDetailCandleListAPIView.as_view()),
]
