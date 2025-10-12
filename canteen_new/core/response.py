"""
统一响应格式模块
"""
from typing import Any, Dict, Optional
from rest_framework.response import Response
from rest_framework import status


class APIResponse:
    """统一API响应格式"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "操作成功",
        pagination: Optional[Dict] = None
    ) -> Response:
        """成功响应"""
        response_data = {
            "success": True,
            "data": data,
            "message": message
        }
        
        if pagination:
            response_data["pagination"] = pagination
            
        return Response(response_data, status=status.HTTP_200_OK)
    
    @staticmethod
    def created(
        data: Any = None,
        message: str = "创建成功"
    ) -> Response:
        """创建成功响应"""
        return Response({
            "success": True,
            "data": data,
            "message": message
        }, status=status.HTTP_201_CREATED)
    
    @staticmethod
    def error(
        error_code: str,
        error_details: str,
        message: str = "操作失败",
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Response:
        """错误响应"""
        return Response({
            "success": False,
            "message": message,
            "error": {
                "code": error_code,
                "details": error_details
            }
        }, status=status_code)
    
    @staticmethod
    def not_found(
        resource: str = "资源"
    ) -> Response:
        """资源未找到响应"""
        return APIResponse.error(
            error_code="NOT_FOUND_001",
            error_details=f"{resource}不存在",
            message="资源未找到",
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized(
        message: str = "认证失败"
    ) -> Response:
        """未认证响应"""
        # 使用400而不是401，避免浏览器自动重定向
        return APIResponse.error(
            error_code="AUTH_001",
            error_details="用户认证失败",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def forbidden(
        message: str = "权限不足"
    ) -> Response:
        """权限不足响应"""
        return APIResponse.error(
            error_code="AUTH_003",
            error_details="用户权限不足",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )
    
    @staticmethod
    def validation_error(
        error_details: str = "参数验证失败"
    ) -> Response:
        """参数验证失败响应"""
        return APIResponse.error(
            error_code="VALIDATION_001",
            error_details=error_details,
            message="参数验证失败",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def server_error(
        error_details: str = "服务器内部错误"
    ) -> Response:
        """服务器错误响应"""
        return APIResponse.error(
            error_code="SERVER_001",
            error_details=error_details,
            message="服务器内部错误",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 创建便捷函数
def api_success(data=None, message="操作成功", pagination=None):
    return APIResponse.success(data, message, pagination)

def api_created(data=None, message="创建成功"):
    return APIResponse.created(data, message)

def api_error(error_code, error_details, message="操作失败", status_code=status.HTTP_400_BAD_REQUEST):
    return APIResponse.error(error_code, error_details, message, status_code)

def api_not_found(resource="资源"):
    return APIResponse.not_found(resource)

def api_unauthorized(message="认证失败"):
    return APIResponse.unauthorized(message)

def api_forbidden(message="权限不足"):
    return APIResponse.forbidden(message)

def api_validation_error(error_details="参数验证失败"):
    return APIResponse.validation_error(error_details)

def api_server_error(error_details="服务器内部错误"):
    return APIResponse.server_error(error_details)
