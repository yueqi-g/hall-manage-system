"""
菜品相关API路由配置
"""
from django.urls import path, re_path
from .dishes import dish_search, dish_filter, popular_dishes, ai_recommend, dish_detail

urlpatterns = [
    re_path(r'^search/?$', dish_search, name='dish_search'),
    re_path(r'^filter/?$', dish_filter, name='dish_filter'),
    re_path(r'^popular/?$', popular_dishes, name='popular_dishes'),
    re_path(r'^ai-recommend/?$', ai_recommend, name='ai_recommend'),
    re_path(r'^(?P<dish_id>\d+)/?$', dish_detail, name='dish_detail'),
]

