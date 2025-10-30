"""
菜品相关API模块
实现菜品搜索、筛选、AI智能推荐、热门推荐等功能
"""
from rest_framework.decorators import api_view
from rest_framework import status

from core.response import api_success, api_error, api_validation_error
from core.exceptions import ValidationException, BusinessException
from data.services import dish_service


@api_view(['GET'])
def dish_search(request):
    """
    菜品搜索
    GET /api/dishes/search?q={query}&page={page}&limit={limit}
    """
    try:
        # 获取查询参数
        query = request.GET.get('q', '')
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        ordering = request.GET.get('ordering', 'default')
        
        # 构建过滤条件
        filters = {
            'page': page,
            'limit': limit,
            'ordering': ordering
        }
        
        # 添加额外的筛选条件（从搜索结果页应用筛选）
        if request.GET.get('price_min'):
            filters['priceMin'] = float(request.GET.get('price_min'))
        if request.GET.get('price_max'):
            filters['priceMax'] = float(request.GET.get('price_max'))
        if request.GET.get('spice_level'):
            filters['spice_level'] = request.GET.get('spice_level')
        if request.GET.get('crowd_level'):
            filters['crowd_level'] = request.GET.get('crowd_level')
        if request.GET.get('hall'):
            filters['hall'] = request.GET.get('hall')
        
        # 调用服务层进行搜索
        result = dish_service.search_dishes_service(query, filters)
        
        return api_success(result, "搜索成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def dish_suggestions(request):
    """
    搜索建议
    GET /api/dishes/suggestions?q={query}
    """
    try:
        # 获取查询参数
        query = request.GET.get('q', '')
        
        if not query or len(query) < 2:
            return api_success([], "搜索建议为空")
        
        # 调用服务层获取搜索建议
        suggestions = dish_service.get_search_suggestions(query)
        
        return api_success(suggestions, "获取搜索建议成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def dish_filter(request):
    """
    菜品筛选
    GET /api/dishes/filter?category={category}&tastes={tastes}&price_min={min}&price_max={max}
    """
    try:
        # 获取筛选条件
        criteria = {
            'category': request.GET.get('category', ''),
            'taste': request.GET.get('tastes', ''),  # 保持taste字段名，与数据库查询一致
            'priceMin': float(request.GET.get('price_min', 0)) if request.GET.get('price_min') else None,
            'priceMax': float(request.GET.get('price_max', 999)) if request.GET.get('price_max') else None,
            'spice_level': request.GET.get('spice_level', ''),
            'crowd_level': request.GET.get('crowd_level', ''),  # 添加人流量筛选
            'hall': request.GET.get('hall', ''),
            'ordering': request.GET.get('ordering', 'default')
        }
        
        print(f"筛选请求 - 原始参数: {dict(request.GET)}")
        print(f"筛选请求 - 处理后的criteria: {criteria}")
        
        # 移除空值
        criteria = {k: v for k, v in criteria.items() if v not in ['', None]}
        
        print(f"筛选请求 - 移除空值后: {criteria}")
        
        # 调用服务层进行筛选
        result = dish_service.filter_dishes_service(criteria)
        
        print(f"筛选结果 - 菜品数量: {len(result.get('dishes', []))}")
        
        return api_success(result, "筛选成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        print(f"筛选错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def popular_dishes(request):
    """
    热门推荐
    GET /api/dishes/popular
    """
    try:
        # 调用服务层获取热门菜品
        dishes = dish_service.get_popular_dishes()
        
        return api_success({"dishes": dishes}, "获取热门菜品成功")
        
    except Exception as e:
        return api_error("SERVER_001", str(e), "获取热门菜品错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def random_dishes(request):
    """
    随机菜品推荐
    GET /api/dishes/random?limit={limit}
    """
    try:
        # 获取参数，默认返回5个菜品
        limit = int(request.GET.get('limit', 5))
        
        # 限制最大数量
        if limit > 20:
            limit = 20
        
        # 调用服务层获取随机菜品
        dishes = dish_service.get_random_dishes(limit)
        
        return api_success({"dishes": dishes}, "获取随机菜品成功")
        
    except Exception as e:
        return api_error("SERVER_001", str(e), "获取随机菜品错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def ai_recommend(request):
    """
    AI智能推荐 - 重构版本（使用新的编排器）
    POST /api/dishes/ai-recommend
    """
    try:
        query = request.data.get('query', '')
        preferences = request.data.get('preferences', {})
        
        if not query:
            return api_validation_error("查询内容不能为空")
        
        # 获取用户ID（如果已登录）
        user_id = None
        if request.user and request.user.is_authenticated:
            user_id = request.user.id
        
        # 调用新的AI编排器
        from ai.orchestrator import ai_orchestrator
        result = ai_orchestrator.process_query(query, user_id)
        
        # 添加API调用状态信息
        enhanced_result = {
            **result,
            "api_status": {
                "processing_mode": result.get("processing_mode", "unknown"),
                "context_aware": True,
                "user_preferences_used": user_id is not None,
                "timestamp": "2025-10-19T11:56:00Z"  # 更新时间戳
            }
        }
        
        return api_success(enhanced_result, "AI推荐成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def dish_detail(request, dish_id):
    """
    菜品详情
    GET /api/dishes/{id}/
    """
    try:
        from data.repositories import DishRepository
        dish_repo = DishRepository()
        
        dish = dish_repo.get_dish_by_id(dish_id)
        
        if not dish:
            return api_error("DISH_001", "菜品不存在", "菜品不存在", status.HTTP_404_NOT_FOUND)
        
        return api_success(dish, "获取菜品详情成功")
        
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)
