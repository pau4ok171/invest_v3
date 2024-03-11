from django.urls import path, include

from . import views

app_name = 'invest'

urlpatterns = [
    path('stocks/', views.InvestCompanyListView.as_view(), name='company_list'),
    path('stocks/detail/<slug>/', views.InvestCompanyDetailView.as_view(), name='company_detail'),
    path(
        'stocks/<slug:country_iso>/',
        views.InvestCompanyListView.as_view(),
        name='company_list_with_one_option'
    ),
    path(
        'stocks/<slug:country_iso>/<slug:sorter_slug>/',
        views.InvestCompanyListView.as_view(),
        name='company_list_with_two_options'
    ),
    path(
        'stocks/<slug:country_iso>/<slug:sector_slug>/<slug:sorter_slug>/',
        views.InvestCompanyListView.as_view(),
        name='company_list_with_all_options'
    ),
    path('api/v1/', include('invest.api.urls', namespace='invest_api')),
]
