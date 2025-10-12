"""
商家管理API模块
实现商家菜品列表、添加菜品、更新菜品、删除菜品、客流量上报等功能
"""
from rest_framework.decorators import api_view
from rest_framework import status

from core.response import api_success, api_error, api_validation_error
from core.exceptions import ValidationException, BusinessException
from data.services import merchant_service
from data.repositories import DishRepository, MerchantRepository


@api_view(['GET'])
def merchant_dishes(request):
    """
    商家菜品列表
    GET /api/merchants/dishes?merchant={merchant_id}
    """
    try:
        # 从查询参数获取商家ID
        merchant_id = request.GET.get('merchant')
        
        if not merchant_id:
            return api_validation_error("商家ID不能为空")
        
        dish_repo = DishRepository()
        dishes = dish_repo.get_dishes_by_merchant(int(merchant_id))
        
        return api_success({"dishes": dishes}, "获取菜品列表成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        print(f"获取商家菜品列表错误: {str(e)}")
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_dish(request):
    """
    添加菜品
    POST /api/merchants/dishes
    """
    try:
        # 验证必填字段
        required_fields = ['merchant', 'name', 'price', 'category', 'taste']
        for field in required_fields:
            if not request.data.get(field):
                return api_validation_error(f"{field}不能为空")
        
        # 获取商家ID
        merchant_id = request.data.get('merchant')
        
        # 准备菜品数据
        dish_data = {
            "merchantId": merchant_id,
            "name": request.data.get('name').strip(),  # 去除首尾空格
            "description": request.data.get('description', ''),
            "price": float(request.data.get('price')),
            "category": request.data.get('category'),
            "taste": request.data.get('taste'),
            "spice_level": int(request.data.get('spice_level', 0)),
            "image_url": request.data.get('image_url', ''),
            "is_available": request.data.get('is_available', True),
            "stock_quantity": int(request.data.get('stock_quantity', 0))
        }
        
        # 调用服务层添加菜品
        result = merchant_service.manage_dishes_service(
            merchant_id=merchant_id,
            action='create',
            data=dish_data
        )
        
        return api_success(result, "菜品添加成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except BusinessException as e:
        return api_error("BUSINESS_001", str(e), str(e))
    except Exception as e:
        error_message = str(e)
        print(f"添加菜品错误: {error_message}")
        import traceback
        traceback.print_exc()
        
        # 检查是否是重复菜品名称错误
        if 'Duplicate entry' in error_message or 'unique_merchant_dish' in error_message:
            return api_error("DUPLICATE_DISH", "该菜品已存在", "您已经添加过同名菜品，请修改菜品名称", status.HTTP_400_BAD_REQUEST)
        
        return api_error("SERVER_001", error_message, "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_dish(request, dish_id):
    """
    更新菜品
    PUT /api/merchants/dishes/{id}
    """
    try:
        # 获取商家ID（从请求中或从菜品信息中获取）
        merchant_id = request.data.get('merchant_id')
        
        if not merchant_id:
            return api_validation_error("商家ID不能为空")
        
        # 准备更新数据
        update_data = {
            "id": dish_id,
            "name": request.data.get('name'),
            "description": request.data.get('description'),
            "price": request.data.get('price'),
            "category": request.data.get('category'),
            "taste": request.data.get('taste'),
            "spice_level": request.data.get('spice_level'),
            "image_url": request.data.get('image_url'),
            "is_available": request.data.get('is_available'),
            "stock_quantity": request.data.get('stock_quantity')
        }
        
        # 移除None值
        update_data = {k: v for k, v in update_data.items() if v is not None}
        
        # 调用服务层更新菜品
        result = merchant_service.manage_dishes_service(
            merchant_id=merchant_id,
            action='update',
            data=update_data
        )
        
        return api_success(result, "菜品更新成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except BusinessException as e:
        return api_error("BUSINESS_001", str(e), str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_dish(request, dish_id):
    """
    删除菜品
    DELETE /api/merchants/dishes/{id}
    """
    try:
        # 获取商家ID
        merchant_id = request.data.get('merchant_id') or request.GET.get('merchant_id')
        
        if not merchant_id:
            # 尝试从菜品信息中获取商家ID
            dish_repo = DishRepository()
            dish = dish_repo.get_dish_by_id(dish_id)
            if dish:
                merchant_id = dish['merchant_id']
            else:
                return api_error("DISH_001", "菜品不存在", "菜品不存在", status.HTTP_404_NOT_FOUND)
        
        # 调用服务层删除菜品
        result = merchant_service.manage_dishes_service(
            merchant_id=merchant_id,
            action='delete',
            data={"id": dish_id}
        )
        
        return api_success(result, "菜品删除成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except BusinessException as e:
        return api_error("BUSINESS_001", str(e), str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def report_traffic(request):
    """
    客流量上报
    POST /api/merchants/traffic
    """
    try:
        # 从请求数据或Token中获取商家ID
        merchant_id = request.data.get('merchant_id')
        
        # 如果没有传merchant_id，尝试从当前用户信息获取
        if not merchant_id:
            # 从localStorage获取的用户信息中获取merchantId
            # 前端应该在请求中包含merchant_id
            return api_validation_error("商家ID不能为空")
        
        # 验证必填字段
        count = request.data.get('count')
        waiting_time = request.data.get('waitingTime')
        
        if count is None or waiting_time is None:
            return api_validation_error("客流量人数和等待时间不能为空")
        
        # 准备客流量数据
        traffic_data = {
            "count": int(count),
            "waitingTime": float(waiting_time),
            "timestamp": request.data.get('timestamp')
        }
        
        # 调用服务层上报客流量
        result = merchant_service.report_traffic_service(merchant_id, traffic_data)
        
        return api_success(result, "客流量信息更新成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        print(f"客流量上报错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def merchant_list(request):
    """
    商家列表查询
    GET /api/merchants/?search={username}
    """
    try:
        search = request.GET.get('search', '')
        hall = request.GET.get('hall', '')
        
        merchant_repo = MerchantRepository()
        
        if search:
            # 按用户名搜索
            merchant = merchant_repo.get_merchant_by_username(search)
            if merchant:
                return api_success({"results": [merchant], "count": 1}, "查询成功")
            else:
                return api_success({"results": [], "count": 0}, "未找到商家")
        elif hall:
            # 按食堂筛选
            merchants = merchant_repo.get_merchants_by_hall(hall)
            return api_success({"results": merchants, "count": len(merchants)}, "查询成功")
        else:
            return api_success({"results": [], "count": 0}, "请提供搜索条件")
        
    except Exception as e:
        print(f"查询商家错误: {str(e)}")
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)

