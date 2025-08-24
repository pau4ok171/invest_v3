from dj_rest_auth.views import PasswordResetConfirmView

from django.urls import path, include

from . import views

urlpatterns = [
    path('password/reset/confirm/<uid64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', include('dj_rest_auth.urls')),
    path('registration/validate-username/', views.validate_username),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('google/', views.GoogleLogin.as_view(), name='google_login'),
    path('yandex/', views.YandexLogin.as_view(), name='yandex_login'),
    path('github/', views.GitHubLogin.as_view(), name='github_login'),
]
