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
        if request.method == 'GET':
            # 从查询参数获取用户ID
            user_id = request.GET.get('userId')
            
            if not user_id:
                return api_validation_error("用户ID不能为空")
            
            # 获取用户偏好
            preferences = user_service.get_user_preferences(int(user_id))
            
            if preferences is not None:
                return api_success(preferences, "获取用户偏好成功")
            else:
                return api_not_found("用户")
                
        elif request.method == 'PUT':
            # 从请求数据获取用户ID
            user_id = request.data.get('userId')
            preferences = request.data.get('preferences', {})
            
            # 验证必要字段
            if not user_id:
                return api_validation_error("用户ID不能为空")
            
            if not preferences:
                return api_validation_error("偏好设置不能为空")
            
            # 调用服务层更新用户偏好
            result = user_service.update_user_preferences(int(user_id), preferences)
            
            if result is not None:
                return api_success(result, "更新用户偏好成功")
            else:
                return api_error("USER_001", "更新用户偏好失败", "更新用户偏好失败")
                
    except Exception as e:
        print(f"用户偏好操作失败: {str(e)}")
        return api_server_error("用户偏好操作失败")
