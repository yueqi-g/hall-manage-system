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

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]

# API文档 - 注释掉避免coreapi依赖问题
# from rest_framework.documentation import include_docs_urls
# urlpatterns += [
#     path('api/docs/', include_docs_urls(title='食堂管理系统API')),
# ]