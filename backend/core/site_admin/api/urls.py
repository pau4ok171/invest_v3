from django.urls import path
from . import views

app_name = 'admin_api'

urlpatterns = [
    path('companies/', views.CompaniesListAPIView.as_view()),
]