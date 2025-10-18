"""
数据服务层 - 业务逻辑实现
包含认证服务、菜品服务、订单服务、商家服务等业务逻辑
"""
from typing import Dict, Any, Optional, List
from .repositories import UserRepository, MerchantRepository, DishRepository, OrderRepository
from core.exceptions import ValidationException, AuthenticationException, BusinessException
from core.security import hash_password, verify_password


class AuthService:
    """认证服务"""
    
    def __init__(self):
        self.user_repo = UserRepository()
        self.merchant_repo = MerchantRepository()
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        用户认证
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            用户信息和认证令牌
            
        Raises:
            AuthenticationException: 认证失败
            ValidationException: 参数验证失败
        """
        if not username or not password:
            raise ValidationException("用户名和密码不能为空")
        
        # 查询用户
        user = self.user_repo.get_user_by_username(username)
        if not user:
            raise AuthenticationException("用户名或密码错误")
        
        # 验证密码
        if not verify_password(password, user['password']):
            raise AuthenticationException("用户名或密码错误")
        
        # 检查用户类型
        if user['type'] != 'user':
            raise AuthenticationException("非普通用户账号")
        
        # 生成认证令牌（简化处理，实际项目中应该使用真正的JWT）
        token = f"jwt_token_{user['id']}"
        
        return {
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user.get('email', ''),
                "type": user['type'],
                "avatar": user.get('avatar', '')
            },
            "token": token
        }
    
    def authenticate_merchant(self, username: str, password: str) -> Dict[str, Any]:
        """
        商家认证
        
        Args:
            username: 商家账号
            password: 密码
            
        Returns:
            商家信息和认证令牌
            
        Raises:
            AuthenticationException: 认证失败
            ValidationException: 参数验证失败
        """
        if not username or not password:
            raise ValidationException("商家账号和密码不能为空")
        
        # 查询商家
        merchant = self.merchant_repo.get_merchant_by_username(username)
        if not merchant:
            raise AuthenticationException("商家账号或密码错误")
        
        # 获取对应的用户信息（用于密码验证）
        user = self.user_repo.get_user_by_username(username)
        if not user or not verify_password(password, user['password']):
            raise AuthenticationException("商家账号或密码错误")
        
        # 检查用户类型
        if user['type'] != 'merchant':
            raise AuthenticationException("非商家账号")
        
        # 生成认证令牌
        token = f"jwt_token_{user['id']}"
        
        return {
            "merchant": {
                "id": merchant['id'],
                "merchantId": merchant['id'],  # 添加merchantId字段
                "username": merchant['username'],
                "storeName": merchant['storeName'],
                "type": "merchant",
                "canteen": merchant['canteen']
            },
            "token": token
        }
    
    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        用户注册
        
        Args:
            user_data: 用户注册数据
            
        Returns:
            新用户信息
            
        Raises:
            ValidationException: 参数验证失败
            BusinessException: 业务逻辑错误
        """
        # 验证必填字段
        required_fields = ['type', 'username', 'password', 'confirmPassword', 'email']
        for field in required_fields:
            if not user_data.get(field):
                raise ValidationException(f"{field}不能为空")
        
        # 验证密码一致性
        if user_data['password'] != user_data['confirmPassword']:
            raise ValidationException("密码和确认密码不一致")
        
        # 检查用户名是否已存在
        existing_user = self.user_repo.get_user_by_username(user_data['username'])
        if existing_user:
            raise BusinessException("用户名已存在")
        
        # 如果是商家注册，验证额外字段
        if user_data['type'] == 'merchant':
            if not user_data.get('storeName') or not user_data.get('canteen'):
                raise ValidationException("商家注册需要提供店铺名称和所属食堂")
        
        # 创建用户数据
        new_user_data = {
            "username": user_data['username'],
            "password": hash_password(user_data['password']),  # 存储哈希密码
            "email": user_data['email'],
            "type": user_data['type']
        }
        
        # 先创建用户记录
        new_user = self.user_repo.create_user(new_user_data)
        
        if not new_user:
            raise BusinessException("用户创建失败")
        
        # 如果是商家，再创建商家记录
        if user_data['type'] == 'merchant':
            merchant_data = {
                "username": user_data['username'],
                "storeName": user_data['storeName'],
                "canteen": user_data['canteen']
            }
            merchant = self.merchant_repo.create_merchant(merchant_data)
            
            if not merchant:
                # 如果商家记录创建失败，需要回滚用户记录
                # 这里简化处理，实际项目应使用数据库事务
                raise BusinessException("商家信息创建失败")
        
        return {
            "id": new_user['id'],
            "username": new_user['username']
        }


class DishService:
    """菜品服务"""
    
    def __init__(self):
        self.dish_repo = DishRepository()
    
    def search_dishes_service(self, query: str, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        菜品搜索服务
        
        Args:
            query: 搜索关键词
            filters: 筛选条件
            
        Returns:
            搜索结果和分页信息
        """
        if filters is None:
            filters = {}
        
        # 调用数据访问层进行搜索
        dishes, pagination = self.dish_repo.search_dishes(query, filters)
        
        return {
            "dishes": dishes,
            "pagination": pagination
        }
    
    def filter_dishes_service(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        菜品筛选服务
        
        Args:
            criteria: 筛选条件
            
        Returns:
            筛选结果和筛选条件
        """
        # 调用数据访问层进行筛选
        dishes = self.dish_repo.filter_dishes(criteria)
        
        return {
            "dishes": dishes,
            "filters": criteria
        }
    
    def get_popular_dishes(self) -> List[Dict[str, Any]]:
        """
        获取热门菜品
        
        Returns:
            热门菜品列表
        """
        return self.dish_repo.get_popular_dishes()
    
    def get_search_suggestions(self, query: str) -> List[str]:
        """
        获取搜索建议
        
        Args:
            query: 搜索关键词
            
        Returns:
            搜索建议列表
        """
        return self.dish_repo.get_search_suggestions(query)
    
    def get_dishes_by_criteria(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        根据多种条件查询菜品
        
        Args:
            criteria: 查询条件
            
        Returns:
            符合条件的菜品列表
        """
        # 调用数据访问层进行筛选
        dishes = self.dish_repo.filter_dishes(criteria)
        
        # 应用评分筛选
        if criteria.get('min_rating') is not None:
            dishes = [dish for dish in dishes if dish.get('rating', 0) >= criteria['min_rating']]
        
        # 应用数量限制
        limit = criteria.get('limit', 10)
        if limit and len(dishes) > limit:
            dishes = dishes[:limit]
        
        return dishes
    
    def add_to_favorites(self, user_id: int, dish_id: int) -> Dict[str, Any]:
        """
        添加菜品到收藏
        
        Args:
            user_id: 用户ID
            dish_id: 菜品ID
            
        Returns:
            收藏信息
        """
        from .repositories import OrderRepository
        order_repo = OrderRepository()
        
        # 添加收藏
        favorite = order_repo.add_favorite(user_id, dish_id)
        
        return favorite
    
    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """
        获取用户收藏列表
        
        Args:
            user_id: 用户ID
            
        Returns:
            收藏菜品列表
        """
        from .repositories import OrderRepository
        order_repo = OrderRepository()
        
        # 获取收藏列表
        favorites = order_repo.get_user_favorites(user_id)
        
        return favorites
    
    def get_user_favorites_summary(self, user_id: int) -> Dict[str, Any]:
        """
        获取用户收藏汇总分析
        
        Args:
            user_id: 用户ID
            
        Returns:
            收藏分析结果，包含类别偏好和口味偏好
        """
        from .repositories import OrderRepository
        order_repo = OrderRepository()
        
        # 获取收藏列表
        favorites = order_repo.get_user_favorites(user_id)
        
        # 分析收藏偏好
        category_count = {}
        taste_count = {}
        
        for favorite in favorites:
            dish = self.dish_repo.get_dish_by_id(favorite['dish_id'])
            if dish:
                # 统计类别偏好
                category = dish.get('category', '其他')
                category_count[category] = category_count.get(category, 0) + 1
                
                # 统计口味偏好
                taste = dish.get('taste', '咸')
                taste_count[taste] = taste_count.get(taste, 0) + 1
        
        # 按频率排序
        preferred_categories = sorted(category_count.keys(), 
                                    key=lambda x: category_count[x], reverse=True)
        preferred_tastes = sorted(taste_count.keys(), 
                                 key=lambda x: taste_count[x], reverse=True)
        
        # 计算预算范围（基于收藏菜品价格）
        prices = []
        for favorite in favorites:
            dish = self.dish_repo.get_dish_by_id(favorite['dish_id'])
            if dish and dish.get('price'):
                prices.append(dish['price'])
        
        if prices:
            budget_range = [min(prices), max(prices)]
        else:
            budget_range = [15, 30]  # 默认预算范围
        
        return {
            "preferred_categories": preferred_categories[:3],  # 取前3个
            "preferred_tastes": preferred_tastes[:2],  # 取前2个
            "budget_range": budget_range,
            "spice_tolerance": self._infer_spice_tolerance(taste_count),
            "favorite_dishes": [favorite['dish_name'] for favorite in favorites[:5]],  # 取前5个菜品名称
            "total_favorites": len(favorites)
        }
    
    def _infer_spice_tolerance(self, taste_count: Dict[str, int]) -> str:
        """
        根据口味偏好推断辣度耐受度
        
        Args:
            taste_count: 口味统计
            
        Returns:
            辣度耐受度描述
        """
        spicy_count = taste_count.get('辣', 0)
        total_count = sum(taste_count.values())
        
        if total_count == 0:
            return "中等"
        
        spicy_ratio = spicy_count / total_count
        
        if spicy_ratio > 0.7:
            return "高"
        elif spicy_ratio > 0.3:
            return "中等"
        else:
            return "低"
    
    def get_crowd_statistics(self, date: str = None, hour: int = None) -> Dict[str, Any]:
        """
        获取客流统计信息
        
        Args:
            date: 日期 (YYYY-MM-DD格式)，默认为今天
            hour: 小时 (0-23)，默认为当前小时
            
        Returns:
            客流统计信息
        """
        try:
            # 如果没有提供日期和时间，使用当前值
            if date is None:
                import datetime
                date = datetime.date.today().strftime('%Y-%m-%d')
            if hour is None:
                hour = datetime.datetime.now().hour
            
            # 从数据库获取客流数据
            # 这里简化处理，实际项目中应该从客流记录表中查询
            from .repositories import MerchantRepository
            merchant_repo = MerchantRepository()
            
            # 获取指定日期和小时的客流数据
            traffic_data = merchant_repo.get_traffic_statistics()
            
            if traffic_data:
                # 计算平均等待时间和客流等级
                avg_wait_time = traffic_data.get('avg_waiting_time', 15)
                avg_count = traffic_data.get('avg_count', 10)
                
                # 根据平均人数确定客流等级
                if avg_count > 30:
                    crowd_level = "高"
                elif avg_count > 15:
                    crowd_level = "中等"
                else:
                    crowd_level = "低"
                
                return {
                    "crowd_level": crowd_level,
                    "avg_wait_time": avg_wait_time,
                    "peak_hours": [11, 12, 13, 17, 18, 19]
                }
            else:
                # 如果没有数据，返回None让调用方处理
                return None
                
        except Exception as e:
            print(f"获取客流统计失败: {e}")
            return None
    
    def remove_from_favorites(self, user_id: int, favorite_id: int) -> bool:
        """
        从收藏中移除菜品
        
        Args:
            user_id: 用户ID
            favorite_id: 收藏ID
            
        Returns:
            是否成功移除
        """
        # 这里简化处理，实际项目中应该验证用户权限
        # 暂时返回True表示成功
        return True


class OrderService:
    """订单服务"""
    
    def __init__(self):
        self.order_repo = OrderRepository()
        self.dish_repo = DishRepository()
    
    def create_order_service(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建订单服务
        
        Args:
            order_data: 订单数据
            
        Returns:
            订单信息
            
        Raises:
            ValidationException: 参数验证失败
            BusinessException: 业务逻辑错误
        """
        # 验证必填字段
        if not order_data.get('dishId'):
            raise ValidationException("菜品ID不能为空")
        
        # 验证菜品是否存在
        dish = self.dish_repo.get_dish_by_id(order_data['dishId'])
        if not dish:
            raise BusinessException("菜品不存在")
        
        # 创建订单
        order = self.order_repo.create_order(order_data)
        
        return {
            "orderId": order['id'],
            "status": "pending",
            "estimatedWaitTime": dish.get('waitTime', 15),
            "totalPrice": dish['price'] * order_data.get('quantity', 1)
        }
    
    def add_favorite_service(self, user_id: int, dish_id: int) -> Dict[str, Any]:
        """
        添加收藏服务
        
        Args:
            user_id: 用户ID
            dish_id: 菜品ID
            
        Returns:
            收藏信息
            
        Raises:
            ValidationException: 参数验证失败
            BusinessException: 业务逻辑错误
        """
        if not user_id or not dish_id:
            raise ValidationException("用户ID和菜品ID不能为空")
        
        # 验证菜品是否存在
        dish = self.dish_repo.get_dish_by_id(dish_id)
        if not dish:
            raise BusinessException("菜品不存在")
        
        # 添加收藏
        favorite = self.order_repo.add_favorite(user_id, dish_id)
        
        return {
            "favoriteId": favorite['id']
        }


class MerchantService:
    """商家服务"""
    
    def __init__(self):
        self.merchant_repo = MerchantRepository()
        self.dish_repo = DishRepository()
    
    def manage_dishes_service(self, merchant_id: int, action: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        管理菜品服务
        
        Args:
            merchant_id: 商家ID
            action: 操作类型 (create|update|delete)
            data: 操作数据
            
        Returns:
            操作结果
            
        Raises:
            ValidationException: 参数验证失败
            BusinessException: 业务逻辑错误
        """
        if not merchant_id:
            raise ValidationException("商家ID不能为空")
        
        if action == 'create':
            # 验证必填字段
            required_fields = ['name', 'price', 'category', 'taste']
            for field in required_fields:
                if not data.get(field):
                    raise ValidationException(f"{field}不能为空")
            
            # 添加商家ID
            data['merchantId'] = merchant_id
            dish = self.dish_repo.create_dish(data)
            
            return {
                "id": dish['id'],
                "name": dish['name'],
                "price": dish['price']
            }
        
        elif action == 'update':
            if not data.get('id'):
                raise ValidationException("菜品ID不能为空")
            
            dish = self.dish_repo.update_dish(data['id'], data)
            return dish
        
        elif action == 'delete':
            if not data.get('id'):
                raise ValidationException("菜品ID不能为空")
            
            self.dish_repo.delete_dish(data['id'])
            return {}
        
        else:
            raise ValidationException(f"不支持的操作类型: {action}")
    
    def report_traffic_service(self, merchant_id: int, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        客流量上报服务
        
        Args:
            merchant_id: 商家ID
            traffic_data: 客流量数据
            
        Returns:
            上报结果
            
        Raises:
            ValidationException: 参数验证失败
        """
        if not merchant_id:
            raise ValidationException("商家ID不能为空")
        
        if not traffic_data.get('count') and traffic_data.get('count') != 0:
            raise ValidationException("客流量人数不能为空")
            
        if not traffic_data.get('waitingTime') and traffic_data.get('waitingTime') != 0:
            raise ValidationException("等待时间不能为空")
        
        # 添加商家ID
        traffic_data['merchantId'] = merchant_id
        
        # 如果没有提供时间戳，使用当前时间
        if not traffic_data.get('timestamp'):
            from datetime import datetime
            traffic_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 记录客流量
        traffic_record = self.merchant_repo.record_traffic(traffic_data)
        
        if traffic_record:
            return {
                "trafficId": traffic_record['id'],
                "currentTraffic": traffic_record['count'],
                "avgWaitTime": traffic_record['waitingTime'],
                "updatedAt": traffic_record['timestamp']
            }
        else:
            raise BusinessException("客流量上报失败")


# 创建服务实例
auth_service = AuthService()
dish_service = DishService()
order_service = OrderService()
merchant_service = MerchantService()
