from django.contrib import admin
from django.conf.urls import i18n
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18/', include(i18n)),
    path('api/v1/auth/', include('apps.user_auth.urls')),
    path('api/v1/invest/', include('apps.invest.urls', namespace='invest_api')),
    path('api/v1/notes/', include('apps.notes.urls', namespace='notes_api')),
    path('api/v1/portfolios/', include('apps.portfolio.urls', namespace='portfolio_api')),
    path('api/v1/admin/', include('apps.site_admin.urls', namespace='admin_api')),
    path('api/v1/profile/', include('apps.user_profile.urls', namespace='profile_api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
