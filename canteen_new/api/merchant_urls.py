"""
商家管理API路由配置
"""
from django.urls import path, re_path
from .merchant import merchant_dishes, add_dish, update_dish, delete_dish, report_traffic, merchant_list

urlpatterns = [
    # 商家菜品管理
    re_path(r'^dishes/?$', merchant_dishes, name='merchant_dishes'),
    re_path(r'^dishes/add/?$', add_dish, name='add_dish'),
    re_path(r'^dishes/(?P<dish_id>\d+)/?$', update_dish, name='update_dish'),
    re_path(r'^dishes/(?P<dish_id>\d+)/delete/?$', delete_dish, name='delete_dish'),
    
    # 客流量管理
    re_path(r'^traffic/?$', report_traffic, name='report_traffic'),
    
    # 商家查询
    re_path(r'^$', merchant_list, name='merchant_list'),
]

