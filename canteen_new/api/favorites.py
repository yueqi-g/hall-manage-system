"""
收藏相关API模块
实现菜品收藏功能
"""
from rest_framework.decorators import api_view
from rest_framework import status

from core.response import api_success, api_error, api_validation_error
from core.exceptions import ValidationException
from data.services import dish_service


@api_view(['POST'])
def add_favorite(request):
    """
    添加收藏
    POST /api/favorites/add/
    """
    try:
        # 获取请求数据
        dish_id = request.data.get('dishId')
        
        if not dish_id:
            return api_validation_error("菜品ID不能为空")
        
        # 验证菜品是否存在
        from data.repositories import DishRepository
        dish_repo = DishRepository()
        dish = dish_repo.get_dish_by_id(dish_id)
        
        if not dish:
            return api_error("DISH_001", "菜品不存在", "菜品不存在", status.HTTP_404_NOT_FOUND)
        
        # 获取当前用户（模拟实现）
        # 在实际项目中，这里会从token中获取用户ID
        current_user = {
            "id": 1,  # 模拟用户ID
            "username": "test_user"
        }
        
        # 调用服务层添加收藏
        result = dish_service.add_to_favorites(current_user['id'], dish_id)
        
        if result:
            return api_success({
                "favoriteId": result.get('id'),
                "dishId": dish_id,
                "message": "收藏成功"
            }, "收藏成功")
        else:
            return api_error("FAV_001", "收藏失败", "收藏失败", status.HTTP_400_BAD_REQUEST)
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_favorites(request):
    """
    获取用户收藏列表
    GET /api/favorites/
    """
    try:
        # 获取当前用户（模拟实现）
        current_user = {
            "id": 1,  # 模拟用户ID
            "username": "test_user"
        }
        
        # 调用服务层获取收藏列表
        favorites = dish_service.get_user_favorites(current_user['id'])
        
        return api_success({
            "favorites": favorites,
            "total": len(favorites)
        }, "获取收藏列表成功")
        
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def remove_favorite(request, favorite_id):
    """
    移除收藏
    DELETE /api/favorites/{id}/
    """
    try:
        # 获取当前用户（模拟实现）
        current_user = {
            "id": 1,  # 模拟用户ID
            "username": "test_user"
        }
        
        # 调用服务层移除收藏
        result = dish_service.remove_from_favorites(current_user['id'], favorite_id)
        
        if result:
            return api_success({
                "message": "取消收藏成功"
            }, "取消收藏成功")
        else:
            return api_error("FAV_002", "取消收藏失败", "取消收藏失败", status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)
