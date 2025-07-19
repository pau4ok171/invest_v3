from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('user_auth.urls')),
    path('api/v1/invest/', include('invest.urls', namespace='invest_api')),
    path('api/v1/notes/', include('notes.urls', namespace='notes_api')),
    path('api/v1/portfolios/', include('portfolio.urls', namespace='portfolio_api')),
    path('api/v1/admin/', include('site_admin.urls', namespace='admin_api')),
    path('api/v1/profile/', include('user_profile.urls', namespace='profile_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
