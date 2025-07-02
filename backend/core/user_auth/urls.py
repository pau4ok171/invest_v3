from dj_rest_auth.views import PasswordResetConfirmView

from django.urls import path, include

from .views import GoogleLogin

urlpatterns = [
    path('password/reset/confirm/<uid64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('google/', GoogleLogin.as_view(), name='google_login'),
]
