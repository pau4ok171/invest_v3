from django.urls import path
from invest.api import views

app_name = 'invest_api'

urlpatterns = [
    path('search/', views.SearchList.as_view()),
    path('validate_username/', views.validate_username),
    path('price_chart/<slug:company_slug>/', views.PriceChartList.as_view(), name='price_chart'),
    path('price_chart_new/<slug:company_slug>/', views.PriceChartList.as_view(), name='price_chart_new'),
]
