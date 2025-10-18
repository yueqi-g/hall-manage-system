"""
URL configuration for canteen_new project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('api.auth_urls')),
    path('api/dishes/', include('api.dishes_urls')),
    path('api/merchants/', include('api.merchant_urls')),
    path('api/favorites/', include('api.favorites_urls')),
]
