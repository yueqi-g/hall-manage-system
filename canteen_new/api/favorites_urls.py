"""
收藏相关URL配置
"""
from django.urls import path
from .favorites import add_favorite, get_favorites, remove_favorite

urlpatterns = [
    path('add/', add_favorite, name='add_favorite'),
    path('', get_favorites, name='get_favorites'),
    path('<int:favorite_id>/', remove_favorite, name='remove_favorite'),
]
