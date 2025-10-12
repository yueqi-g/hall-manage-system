from rest_framework import viewsets, status, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg, Sum, Min, Max, Case, When, IntegerField
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Merchant, Dish, UserPreference, Order, OrderItem, FootTraffic
from .serializers import *

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'taste', 'merchant', 'is_available']
    search_fields = ['name', 'description', 'merchant__name']
    ordering_fields = ['price', 'created_at', 'spice_level']
    ordering = ['-created_at']

    def get_permissions(self):
        # 只读接口允许匿名，修改类操作需要登录
        if self.action in ['list', 'retrieve', 'filter_dishes', 'popular', 'search_suggestions']:
            return []
        return [IsAuthenticated()]

    def _get_user_merchant(self, user):
        merchant_record = getattr(user, 'merchant_profile', None)
        if merchant_record is None:
            merchant_record = Merchant.objects.filter(name=user.username).first()
        return merchant_record

    def get_queryset(self):
        queryset = Dish.objects.select_related('merchant').filter(is_available=True)
        
        # 获取查询参数
        category = self.request.query_params.get('category')
        tastes = self.request.query_params.getlist('tastes') or self.request.query_params.get('tastes')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        spice_level = self.request.query_params.get('spice_level')
        hall = self.request.query_params.get('hall')
        crowd_level = self.request.query_params.get('crowd_level')
        search_query = self.request.query_params.get('search')
        merchant_param = self.request.query_params.get('merchant')
        
        # 品类筛选
        if category and category != 'all':
            queryset = queryset.filter(category=category)
        
        # 口味筛选（支持多选）
        if tastes:
            if isinstance(tastes, str):
                tastes = tastes.split(',')
            taste_queries = Q()
            for taste in tastes:
                taste_queries |= Q(taste=taste)
            queryset = queryset.filter(taste_queries)
        
        # 价格范围筛选
        if price_min:
            queryset = queryset.filter(price__gte=float(price_min))
        if price_max:
            queryset = queryset.filter(price__lte=float(price_max))
        
        # 辣度筛选
        if spice_level:
            queryset = queryset.filter(spice_level=int(spice_level))
        
        # 食堂筛选
        if hall:
            queryset = queryset.filter(merchant__hall=hall)
        
        # 人流量筛选（基于商家的平均客流量）
        if crowd_level and crowd_level != 'any':
            # 获取符合人流量条件的商家ID
            traffic_queryset = FootTraffic.objects.values('merchant').annotate(
                avg_traffic=Avg('traffic_count')
            )
            
            if crowd_level == 'low':
                merchant_ids = [t['merchant'] for t in traffic_queryset if t['avg_traffic'] < 20]
            elif crowd_level == 'medium':
                merchant_ids = [t['merchant'] for t in traffic_queryset if 20 <= t['avg_traffic'] <= 50]
            elif crowd_level == 'high':
                merchant_ids = [t['merchant'] for t in traffic_queryset if t['avg_traffic'] > 50]
            else:
                merchant_ids = []
            
            queryset = queryset.filter(merchant_id__in=merchant_ids)
        
        # 搜索查询
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(merchant__name__icontains=search_query) |
                Q(category__icontains=search_query) |
                Q(taste__icontains=search_query)
            )
        
        # 只在 list 操作且显式传入 merchant 参数时过滤商家菜品
        # 或者在其他需要商家过滤的特定操作中
        # 对于 filter_dishes、search 等公共查询，不自动应用商家过滤
        if merchant_param:
            try:
                merchant_id = int(merchant_param)
                queryset = queryset.filter(merchant_id=merchant_id)
            except (ValueError, TypeError):
                pass  # 忽略无效的 merchant 参数
        
        return queryset

    def perform_create(self, serializer):
        # 如果未显式提供 merchant，则根据当前登录用户推断商家
        merchant = None
        provided_merchant = self.request.data.get('merchant')
        
        if provided_merchant:
            try:
                # 确保 provided_merchant 是有效的整数
                merchant_id = int(provided_merchant)
                merchant = Merchant.objects.get(pk=merchant_id)
            except (ValueError, TypeError):
                raise ValidationError({'merchant': '商家ID格式错误'})
            except Merchant.DoesNotExist:
                raise ValidationError({'merchant': f'无效的商家ID: {provided_merchant}'})
        else:
            merchant = self._get_user_merchant(self.request.user)
            if not merchant:
                raise ValidationError({'merchant': '无法确定商家，请先绑定商家或提供商家ID'})
        
        # 验证当前用户是否有权限为此商家添加菜品
        user_merchant = self._get_user_merchant(self.request.user)
        if user_merchant and merchant.id != user_merchant.id:
            raise PermissionDenied('无权为其他商家添加菜品')
        
        serializer.save(merchant=merchant)

    def perform_update(self, serializer):
        instance = self.get_object()
        user_merchant = self._get_user_merchant(self.request.user)
        if not user_merchant or instance.merchant_id != user_merchant.id:
            raise PermissionDenied('无权修改其他商家的菜品')
        # 禁止把菜品转移到其他商家
        serializer.save(merchant=user_merchant)

    def perform_destroy(self, instance):
        user_merchant = self._get_user_merchant(self.request.user)
        if not user_merchant or instance.merchant_id != user_merchant.id:
            raise PermissionDenied('无权删除其他商家的菜品')
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def filter_dishes(self, request):
        """
        综合筛选接口 - 支持所有筛选条件
        """
        try:
            queryset = self.get_queryset()
            
            # 分页
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'success': True,
                'count': queryset.count(),
                'dishes': serializer.data,
                'filters_applied': {
                    'category': request.query_params.get('category'),
                    'tastes': request.query_params.getlist('tastes'),
                    'price_min': request.query_params.get('price_min'),
                    'price_max': request.query_params.get('price_max'),
                    'crowd_level': request.query_params.get('crowd_level')
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        获取热门推荐菜品
        """
        try:
            # 基于订单数量计算热门菜品
            popular_dishes = Dish.objects.annotate(
                order_count=Count('orderitem')
            ).filter(
                is_available=True
            ).order_by('-order_count', '-created_at')[:12]
            
            serializer = self.get_serializer(popular_dishes, many=True)
            return Response({
                'success': True,
                'count': popular_dishes.count(),
                'dishes': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def search_suggestions(self, request):
        """
        搜索建议接口
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response([])
        
        # 菜品名称建议
        dish_suggestions = Dish.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True).distinct()[:5]
        
        # 商家名称建议
        merchant_suggestions = Merchant.objects.filter(
            name__icontains=query
        ).values_list('name', flat=True).distinct()[:5]
        
        # 品类建议
        category_suggestions = Dish.objects.filter(
            category__icontains=query
        ).values_list('category', flat=True).distinct()[:5]
        
        suggestions = list(dish_suggestions) + list(merchant_suggestions) + list(category_suggestions)
        
        return Response(suggestions[:10])

class MerchantViewSet(viewsets.ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['hall', 'status']
    search_fields = ['name', 'description']

    def get_queryset(self):
        queryset = Merchant.objects.prefetch_related('dishes')
        
        # 实时状态筛选
        status_filter = self.request.query_params.get('status')
        if status_filter:
            if status_filter.lower() == 'open':
                queryset = queryset.filter(status=True)
            elif status_filter.lower() == 'closed':
                queryset = queryset.filter(status=False)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def traffic_stats(self, request, pk=None):
        """
        获取商家客流量统计
        """
        merchant = self.get_object()
        
        # 今日客流量
        today_traffic = FootTraffic.objects.filter(
            merchant=merchant,
            record_date=timezone.now().date()
        ).aggregate(
            total_traffic=Sum('traffic_count')
        )['total_traffic'] or 0
        
        # 最近7天平均客流量
        week_ago = timezone.now().date() - timezone.timedelta(days=7)
        weekly_avg = FootTraffic.objects.filter(
            merchant=merchant,
            record_date__gte=week_ago
        ).aggregate(
            avg_traffic=Avg('traffic_count')
        )['avg_traffic'] or 0
        
        # 时间段分布
        time_slot_stats = FootTraffic.objects.filter(
            merchant=merchant,
            record_date=timezone.now().date()
        ).values('time_slot').annotate(
            traffic=Sum('traffic_count')
        )
        
        return Response({
            'today_traffic': today_traffic,
            'weekly_avg_traffic': round(weekly_avg, 2),
            'time_slot_stats': list(time_slot_stats)
        })

class FilterOptionsViewSet(viewsets.ViewSet):
    """
    筛选选项数据接口
    """
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """获取所有品类选项"""
        categories = Dish.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))
    
    @action(detail=False, methods=['get'])
    def tastes(self, request):
        """获取所有口味选项"""
        tastes = Dish.objects.values_list('taste', flat=True).distinct()
        return Response(list(tastes))
    
    @action(detail=False, methods=['get'])
    def halls(self, request):
        """获取所有食堂选项"""
        halls = Merchant.objects.values_list('hall', flat=True).distinct()
        return Response(list(halls))
    
    @action(detail=False, methods=['get'])
    def price_ranges(self, request):
        """获取价格范围统计"""
        price_stats = Dish.objects.aggregate(
            min_price=Min('price'),
            max_price=Max('price'),
            avg_price=Avg('price')
        )
        return Response(price_stats)

class UserPreferenceViewSet(viewsets.ModelViewSet):
    """用户偏好管理"""
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    
    def get_queryset(self):
        # 只返回当前用户的偏好设置
        if self.request.user.is_authenticated:
            return UserPreference.objects.filter(user=self.request.user)
        return UserPreference.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    """订单管理"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'user', 'merchant']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Order.objects.select_related('user', 'merchant').prefetch_related('items')
        if self.request.user.is_authenticated:
            # 如果是普通用户，只显示自己的订单
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FootTrafficViewSet(viewsets.ModelViewSet):
    """客流量管理"""
    queryset = FootTraffic.objects.all()
    serializer_class = FootTrafficSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['merchant', 'time_slot']
    ordering_fields = ['record_date', 'traffic_count']
    ordering = ['-record_date']
    
    def get_queryset(self):
        return FootTraffic.objects.select_related('merchant')

class AIServiceViewSet(viewsets.ViewSet):
    """AI服务相关接口"""
    
    @action(detail=False, methods=['post'])
    def recommend_dishes(self, request):
        """AI菜品推荐"""
        # 模拟AI推荐逻辑
        user_preferences = request.data.get('preferences', {})
        query = request.data.get('query', '')
        
        # 基于用户偏好和查询内容推荐菜品
        dishes = Dish.objects.filter(is_available=True)
        
        # 简单的推荐逻辑
        if user_preferences.get('category'):
            dishes = dishes.filter(category=user_preferences['category'])
        
        if user_preferences.get('taste'):
            dishes = dishes.filter(taste=user_preferences['taste'])
        
        # 限制推荐数量
        dishes = dishes[:5]
        
        serializer = DishSerializer(dishes, many=True)
        
        return Response({
            'success': True,
            'data': {
                'recommendations': serializer.data,
                'query': query,
                'reason': '基于您的偏好推荐'
            }
        })
    
    @action(detail=False, methods=['post'])
    def analyze_traffic(self, request):
        """AI客流量分析"""
        merchant_id = request.data.get('merchant_id')
        
        # 模拟AI分析
        analysis_result = {
            'success': True,
            'data': {
                'prediction': '预计下午2-4点客流量较高',
                'recommendation': '建议提前准备食材',
                'confidence': 0.85
            }
        }
        
        return Response(analysis_result)

# 认证相关视图
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import JsonResponse

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """用户登录"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': '用户名和密码不能为空'
        }, status=400)
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'type': 'user'
                },
                'token': token.key
            },
            'message': '登录成功'
        })
    else:
        return Response({
            'success': False,
            'message': '用户名或密码错误'
        }, status=401)

@api_view(['POST'])
@permission_classes([AllowAny])
def merchant_login(request):
    """商家登录"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'success': False,
            'message': '用户名和密码不能为空'
        }, status=400)
    
    user = authenticate(username=username, password=password)
    
    if user:
        # 检查是否是商家用户（这里简化处理，实际应该有商家角色判断）
        token, created = Token.objects.get_or_create(user=user)
        # 优先使用显式的用户-商家关联
        merchant_record = getattr(user, 'merchant_profile', None)
        if merchant_record is None:
            # 回退到按名称匹配
            merchant_record = Merchant.objects.filter(name=user.username).first()
        merchant_id = merchant_record.id if merchant_record else None
        return Response({
            'success': True,
            'data': {
                'merchant': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'type': 'merchant',
                    'merchantId': merchant_id
                },
                'token': token.key
            },
            'message': '商家登录成功'
        })
    else:
        return Response({
            'success': False,
            'message': '商家账号或密码错误'
        }, status=401)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    """用户注册（支持用户和商家注册）"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    register_type = request.data.get('type', 'user')  # 'user' 或 'merchant'
    
    if not username or not password or not email:
        return Response({
            'success': False,
            'message': '注册信息不完整'
        }, status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({
            'success': False,
            'message': '用户名已存在'
        }, status=400)
    
    if User.objects.filter(email=email).exists():
        return Response({
            'success': False,
            'message': '邮箱已被使用'
        }, status=400)
    
    # 如果是商家注册，验证商家专属字段
    if register_type == 'merchant':
        store_name = request.data.get('storeName')
        canteen = request.data.get('canteen')
        
        if not store_name or not canteen:
            return Response({
                'success': False,
                'message': '商家注册需要提供店铺名称和所属食堂'
            }, status=400)
        
        # 检查商家名称是否已存在
        if Merchant.objects.filter(name=store_name).exists():
            return Response({
                'success': False,
                'message': '店铺名称已被使用'
            }, status=400)
    
    try:
        # 创建用户
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # 根据注册类型创建相应的记录
        if register_type == 'merchant':
            # 创建商家记录
            store_name = request.data.get('storeName')
            canteen = request.data.get('canteen')
            
            # 为商家自动分配窗口号（找到可用的最小窗口号）
            existing_merchants = Merchant.objects.filter(hall=canteen).order_by('location')
            used_numbers = []
            for m in existing_merchants:
                # 提取窗口号中的数字
                try:
                    num = int(m.location.replace('窗口', ''))
                    used_numbers.append(num)
                except:
                    pass
            
            # 找到第一个未使用的窗口号
            window_number = 1
            while window_number in used_numbers:
                window_number += 1
            
            location = f'窗口{window_number}'
            
            merchant = Merchant.objects.create(
                user=user,
                name=store_name,
                hall=canteen,
                location=location,
                description=f'{store_name} - 自助注册商家',
                status=True
            )
            
            return Response({
                'success': True,
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'type': 'merchant',
                    'merchantId': merchant.id,
                    'storeName': merchant.name,
                    'hall': merchant.hall,
                    'location': merchant.location
                },
                'message': '商家注册成功！'
            })
        else:
            # 创建用户偏好设置
            UserPreference.objects.create(user=user)
            
            return Response({
                'success': True,
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'type': 'user'
                },
                'message': '用户注册成功！'
            })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'注册失败: {str(e)}'
        }, status=500)