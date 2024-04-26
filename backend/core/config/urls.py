"""
URL configuration for finargo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('invest/', include('invest.urls', namespace='invest')),
    path('watchlist/', include('watchlist.urls', namespace='watchlist')),
    path('portfolio/', include('portfolio.urls', namespace='portfolio')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('', include('django.contrib.auth.urls')),
    path('', views.HomePageView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = views.PageNotFound.as_view()
