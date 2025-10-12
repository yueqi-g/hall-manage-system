from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'merchants', views.MerchantViewSet)
router.register(r'dishes', views.DishViewSet)
router.register(r'user-preferences', views.UserPreferenceViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'foot-traffic', views.FootTrafficViewSet)
router.register(r'ai-services', views.AIServiceViewSet, basename='ai-services')
router.register(r'filter-options', views.FilterOptionsViewSet, basename='filter-options')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # 自定义认证接口
    path('auth/user-login/', views.user_login, name='user_login'),
    path('auth/merchant-login/', views.merchant_login, name='merchant_login'),
    path('auth/register/', views.user_register, name='user_register'),
]

# API文档 (需要安装coreapi)
# from rest_framework.documentation import include_docs_urls
# urlpatterns += [
#     path('api/docs/', include_docs_urls(title='食堂管理系统API')),
# ]