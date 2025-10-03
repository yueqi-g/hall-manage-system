from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from .models import Merchant, Dish, UserPreference, Order, OrderItem, FootTraffic
from .serializers import *

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    
    @action(detail=True, methods=['get'])
    def dishes(self, request, pk=None):
        merchant = self.get_object()
        dishes = merchant.dishes.filter(is_available=True)
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_hall(self, request):
        hall = request.query_params.get('hall')
        merchants = Merchant.objects.filter(hall=hall, status=True)
        serializer = self.get_serializer(merchants, many=True)
        return Response(serializer.data)

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    
    def get_queryset(self):
        queryset = Dish.objects.all()
        # 过滤参数
        category = self.request.query_params.get('category')
        taste = self.request.query_params.get('taste')
        max_price = self.request.query_params.get('max_price')
        merchant_id = self.request.query_params.get('merchant_id')
        available_only = self.request.query_params.get('available_only')
        
        if category:
            queryset = queryset.filter(category=category)
        if taste:
            queryset = queryset.filter(taste=taste)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if merchant_id:
            queryset = queryset.filter(merchant_id=merchant_id)
        if available_only:
            queryset = queryset.filter(is_available=True)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q')
        if query:
            dishes = Dish.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(merchant__name__icontains=query)
            )
            serializer = self.get_serializer(dishes, many=True)
            return Response(serializer.data)
        return Response([])

class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return UserPreference.objects.filter(user=user)
        return UserPreference.objects.none()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        return Order.objects.none()
    
    def create(self, request):
        # 创建订单逻辑
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 这里可以添加AI推荐得分计算
        order = serializer.save()
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class FootTrafficViewSet(viewsets.ModelViewSet):
    queryset = FootTraffic.objects.all()
    serializer_class = FootTrafficSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        merchant_id = request.query_params.get('merchant_id')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        
        queryset = self.get_queryset()
        
        if merchant_id:
            queryset = queryset.filter(merchant_id=merchant_id)
        if date_from:
            queryset = queryset.filter(record_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(record_date__lte=date_to)
        
        # 统计信息
        total_traffic = queryset.aggregate(Sum('traffic_count'))['traffic_count__sum'] or 0
        avg_traffic = queryset.aggregate(Avg('traffic_count'))['traffic_count__avg'] or 0
        
        return Response({
            'total_traffic': total_traffic,
            'average_traffic': round(avg_traffic, 2),
            'record_count': queryset.count()
        })

# AI相关视图
class AIServiceViewSet(viewsets.ViewSet):
    """
    AI服务接口
    """
    
    @action(detail=False, methods=['post'])
    def recommend_dishes(self, request):
        """
        AI菜品推荐
        """
        serializer = AIRecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        user_id = data.get('user_id')
        categories = data.get('categories', [])
        tastes = data.get('tastes', [])
        max_price = data.get('max_price')
        max_results = data.get('max_results', 5)
        
        # 基础查询
        queryset = Dish.objects.filter(is_available=True)
        
        # 应用过滤条件
        if categories:
            queryset = queryset.filter(category__in=categories)
        if tastes:
            queryset = queryset.filter(taste__in=tastes)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # 这里预留AI推荐算法接口
        # 可以集成机器学习模型进行个性化推荐
        recommended_dishes = queryset[:max_results]
        
        # 模拟AI评分（实际项目中会调用AI模型）
        for dish in recommended_dishes:
            dish.ai_score = 0.8  # 模拟AI推荐分数
        
        serializer = DishSerializer(recommended_dishes, many=True)
        
        return Response({
            'recommendations': serializer.data,
            'ai_model_used': 'content_based_filtering',  # 预留AI模型信息
            'recommendation_count': len(recommended_dishes)
        })
    
    @action(detail=False, methods=['post'])
    def predict_traffic(self, request):
        """
        AI客流量预测
        """
        serializer = AIPredictionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        merchant_id = data.get('merchant_id')
        date = data.get('date')
        time_slot = data.get('time_slot')
        
        # 这里预留AI预测算法接口
        # 可以集成时间序列预测模型
        
        # 模拟预测结果
        prediction_data = {
            'predicted_traffic': 150,
            'confidence': 0.85,
            'factors_considered': ['historical_data', 'day_of_week', 'weather'],
            'model_used': 'arima_time_series'
        }
        
        return Response(prediction_data)
    
    @action(detail=False, methods=['post'])
    def analyze_user_behavior(self, request):
        """
        AI用户行为分析
        """
        user_id = request.data.get('user_id')
        
        # 预留用户行为分析接口
        # 可以分析用户偏好、消费习惯等
        
        analysis_result = {
            'user_segment': 'value_seeker',
            'preferred_categories': ['饭', '面'],
            'average_order_value': 25.50,
            'favorite_merchants': [1, 3, 5],
            'behavior_pattern': 'lunch_regular'
        }
        
        return Response(analysis_result)