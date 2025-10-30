"""
URL configuration for canteen_new project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('api.auth_urls')),
    path('api/dishes/', include('api.dishes_urls')),
    path('api/merchants/', include('api.merchant_urls')),
    path('api/favorites/', include('api.favorites_urls')),
    path('api/user/', include('api.user_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
