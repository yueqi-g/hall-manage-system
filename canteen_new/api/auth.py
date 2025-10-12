"""
认证相关API模块
实现用户登录、商家登录、用户注册等功能
"""
from rest_framework.decorators import api_view
from rest_framework import status

from core.response import api_success, api_error, api_validation_error, api_unauthorized
from core.exceptions import ValidationException, AuthenticationException, BusinessException
from data.services import auth_service


@api_view(['POST'])
def user_login(request):
    """
    用户登录
    POST /api/auth/user/login
    """
    try:
        # 验证请求数据
        username = request.data.get('username')
        password = request.data.get('password')
        
        print(f"登录请求 - 用户名: {username}, 密码: {password}")
        
        if not all([username, password]):
            return api_validation_error("用户名和密码不能为空")
        
        # 使用认证服务进行用户认证
        auth_result = auth_service.authenticate_user(username, password)
        
        return api_success(auth_result, "登录成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except AuthenticationException as e:
        return api_unauthorized(str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def merchant_login(request):
    """
    商家登录
    POST /api/auth/merchant/login
    """
    try:
        # 验证请求数据
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not all([username, password]):
            return api_validation_error("商家账号和密码不能为空")
        
        # 使用认证服务进行商家认证
        auth_result = auth_service.authenticate_merchant(username, password)
        
        return api_success(auth_result, "商家登录成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except AuthenticationException as e:
        return api_unauthorized(str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def user_register(request):
    """
    用户注册
    POST /api/auth/register
    """
    try:
        print(f"注册请求 - 接收到的数据: {request.data}")
        
        # 验证请求数据
        register_type = request.data.get('type')
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirmPassword')
        email = request.data.get('email')
        
        print(f"注册请求 - 类型: {register_type}, 用户名: {username}, 邮箱: {email}")
        
        if not all([register_type, username, password, confirm_password, email]):
            return api_validation_error("注册类型、用户名、密码、确认密码和邮箱不能为空")
        
        if password != confirm_password:
            return api_validation_error("密码和确认密码不一致")
        
        # 准备注册数据
        user_data = {
            "type": register_type,
            "username": username,
            "password": password,
            "confirmPassword": confirm_password,
            "email": email
        }
        
        # 如果是商家注册，添加额外信息
        if register_type == 'merchant':
            store_name = request.data.get('storeName')
            canteen = request.data.get('canteen')
            
            print(f"商家注册 - 店铺名称: {store_name}, 食堂: {canteen}")
            
            if not all([store_name, canteen]):
                return api_validation_error("商家注册需要提供店铺名称和所属食堂")
            
            user_data.update({
                "storeName": store_name,
                "canteen": canteen
            })
        
        print(f"注册请求 - 准备调用服务层注册用户...")
        
        # 使用认证服务进行用户注册
        register_result = auth_service.register_user(user_data)
        
        print(f"注册成功 - 用户ID: {register_result.get('id')}")
        
        return api_success(register_result, "注册成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except BusinessException as e:
        return api_error("BUSINESS_001", str(e), str(e))
    except Exception as e:
        print(f"注册错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)
