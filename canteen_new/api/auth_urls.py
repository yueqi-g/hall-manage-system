"""
认证相关API路由配置
"""
from django.urls import path, re_path
from .auth import user_login, merchant_login, user_register

urlpatterns = [
    re_path(r'^user-login/?$', user_login, name='user_login'),
    re_path(r'^merchant-login/?$', merchant_login, name='merchant_login'),
    re_path(r'^register/?$', user_register, name='user_register'),
]
