from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from invest import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    # Invest
    path('invest/', include('invest.urls', namespace='invest')),
    path('api/v1/invest/', include('invest.api.urls', namespace='invest_api')),
    # Notes
    path('notes/', include('notes.urls', namespace='notes')),
    path('api/v1/notes/', include('notes.api.urls', namespace='notes_api')),
    # Portfolio
    path('portfolio/', include('portfolio.urls', namespace='portfolio')),
    path('api/v1/portfolio/', include('portfolio.api.urls', namespace='portfolio_api')),
    # Watchlist
    path('watchlist/', include('watchlist.urls', namespace='watchlist')),
    path('api/v1/watchlist/', include('watchlist.api.urls', namespace='watchlist_api')),
    path('', include('django.contrib.auth.urls')),
    path('api/v1/admin/', include('site_admin.api.urls', namespace='admin_api')),
    path('', views.HomePageView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = views.PageNotFound.as_view()
