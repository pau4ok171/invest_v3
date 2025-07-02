from django.urls import path
from site_admin import views

app_name = 'admin_api'

urlpatterns = [
    path('companies/', views.CompaniesListAPIView.as_view()),
    path('companies/<slug:company_uid>/', views.CompanyAPIView.as_view()),
    path('selector_options/', views.SelectorOptionsAPIView.as_view()),
    path('users/', views.UserRetrieveAPIView.as_view())
]
