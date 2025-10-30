"""
用户相关API接口
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.response import api_success, api_error, api_validation_error, api_unauthorized, api_not_found, api_server_error
from core.exceptions import ValidationException, BusinessException
from data.services import user_service


@api_view(['GET'])
def get_user_profile(request):
    """
    获取用户信息
    GET /api/user/profile/
    """
    try:
        # 从认证信息中获取用户ID
        user_id = None
        if request.user and request.user.is_authenticated:
            user_id = request.user.id
        
        if not user_id:
            return api_unauthorized("用户未登录")
        
        # 调用服务层获取用户信息
        user_info = user_service.get_user_profile(user_id)
        
        if user_info:
            return api_success(user_info, "获取用户信息成功")
        else:
            return api_not_found("用户")
            
    except Exception as e:
        print(f"获取用户信息失败: {str(e)}")
        return api_server_error("获取用户信息失败")


@api_view(['GET', 'PUT'])
def user_preferences(request):
    """
    用户偏好设置API
    GET /api/user/preferences/ - 获取用户偏好设置
    PUT /api/user/preferences/ - 更新用户偏好设置
    """
    try:
        print(f"用户偏好API请求 - 方法: {request.method}")
        print(f"请求数据: {request.data}")
        print(f"查询参数: {request.GET}")
        
        if request.method == 'GET':
            # 从查询参数获取用户ID
            user_id = request.GET.get('userId')
            
            print(f"GET请求 - 用户ID: {user_id}")
            
            if not user_id:
                return api_validation_error("用户ID不能为空")
            
            try:
                user_id_int = int(user_id)
            except ValueError:
                return api_validation_error("无效的用户ID")
            
            # 获取用户偏好
            preferences = user_service.get_user_preferences(user_id_int)
            
            print(f"获取到用户偏好: {preferences}")
            
            if preferences is not None:
                # 如果preferences是空字典，返回默认值
                if not preferences:
                    preferences = {}
                return api_success(preferences, "获取用户偏好成功")
            else:
                return api_not_found("用户")
                
        elif request.method == 'PUT':
            # 从请求数据获取用户ID
            user_id = request.data.get('userId')
            preferences = request.data.get('preferences', {})
            
            print(f"PUT请求 - 用户ID: {user_id}, 偏好数据: {preferences}")
            
            # 验证必要字段
            if not user_id:
                return api_validation_error("用户ID不能为空")
            
            try:
                user_id_int = int(user_id)
            except ValueError:
                return api_validation_error("无效的用户ID")
            
            # 偏好设置可以为空（允许清除偏好）
            
            # 调用服务层更新用户偏好
            result = user_service.update_user_preferences(user_id_int, preferences)
            
            print(f"更新结果: {result}")
            
            if result is not None:
                return api_success(result, "更新用户偏好成功")
            else:
                return api_error("USER_001", "更新用户偏好失败", "更新用户偏好失败")
                
    except ValidationException as e:
        print(f"验证异常: {str(e)}")
        return api_validation_error(str(e))
    except BusinessException as e:
        print(f"业务异常: {str(e)}")
        return api_error("BUSINESS_001", str(e), str(e))
    except Exception as e:
        print(f"用户偏好操作失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)
