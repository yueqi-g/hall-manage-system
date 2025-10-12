"""
异常情况
"""


class APIException(Exception):
    """基础API异常类"""
    
    def __init__(self, error_code: str, error_details: str, message: str = "操作失败"):
        self.error_code = error_code
        self.error_details = error_details
        self.message = message
        super().__init__(self.message)


class AuthenticationException(APIException):
    """认证异常"""
    
    def __init__(self, error_details: str = "用户认证失败", message: str = "认证失败"):
        super().__init__("AUTH_001", error_details, message)


class AuthorizationException(APIException):
    """授权异常"""
    
    def __init__(self, error_details: str = "用户权限不足", message: str = "权限不足"):
        super().__init__("AUTH_003", error_details, message)


class ValidationException(APIException):
    """参数验证异常"""
    
    def __init__(self, error_details: str = "参数验证失败", message: str = "参数验证失败"):
        super().__init__("VALIDATION_001", error_details, message)


class NotFoundException(APIException):
    """资源未找到异常"""
    
    def __init__(self, resource: str = "资源", message: str = "资源未找到"):
        super().__init__("NOT_FOUND_001", f"{resource}不存在", message)


class BusinessException(APIException):
    """业务逻辑异常"""
    
    def __init__(self, error_details: str = "业务逻辑错误", message: str = "业务逻辑错误"):
        super().__init__("BUSINESS_001", error_details, message)


class ServerException(APIException):
    """服务器异常"""
    
    def __init__(self, error_details: str = "服务器内部错误", message: str = "服务器内部错误"):
        super().__init__("SERVER_001", error_details, message)
