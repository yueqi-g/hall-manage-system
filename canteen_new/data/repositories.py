"""
数据访问层
此模块中实现与数据库之间的交互。
"""
from typing import Dict, Any, Optional, List, Tuple
from .database import query_one, query_all, execute_update, execute_insert


class UserRepository:
    """用户数据访问"""
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取用户"""
        query = """
            SELECT id, username, password, email, type, avatar, created_at, updated_at
            FROM users 
            WHERE id = %s AND status = 'active'
        """
        return query_one(query, (user_id,))
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取用户"""
        query = """
            SELECT id, username, password, email, type, avatar, created_at, updated_at
            FROM users 
            WHERE username = %s AND status = 'active'
        """
        return query_one(query, (username,))
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建用户"""
        query = """
            INSERT INTO users (username, password, email, type, avatar, status)
            VALUES (%s, %s, %s, %s, %s, 'active')
        """
        user_id = execute_insert(
            query, 
            (
                user_data['username'],
                user_data['password'],
                user_data.get('email', ''),
                user_data['type'],
                user_data.get('avatar', '')
            )
        )
        
        if user_id:
            return {
                "id": user_id,
                "username": user_data['username'],
                "email": user_data.get('email', ''),
                "type": user_data['type']
            }
        return None
    
    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户偏好设置"""
        # 这里需要根据实际的用户偏好表结构来实现
        # 暂时返回空字典，表示更新成功
        return {}


class MerchantRepository:
    """商家数据访问"""
    
    def get_merchant_by_id(self, merchant_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取商家"""
        query = """
            SELECT id, username, store_name, canteen, location, contact_info, description, status
            FROM merchants 
            WHERE id = %s AND status = 'active'
        """
        result = query_one(query, (merchant_id,))
        if result:
            return {
                "id": result['id'],
                "username": result['username'],
                "storeName": result['store_name'],
                "canteen": result['canteen'],
                "location": result['location'],
                "contact_info": result['contact_info'],
                "description": result['description'],
                "status": result['status']
            }
        return None
    
    def get_merchant_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取商家"""
        query = """
            SELECT id, username, store_name, canteen, location, contact_info, description, status
            FROM merchants 
            WHERE username = %s AND status = 'active'
        """
        result = query_one(query, (username,))
        if result:
            return {
                "id": result['id'],
                "username": result['username'],
                "storeName": result['store_name'],
                "canteen": result['canteen'],
                "location": result['location'],
                "contact_info": result['contact_info'],
                "description": result['description'],
                "status": result['status']
            }
        return None
    
    def get_merchants_by_hall(self, hall: str) -> List[Dict[str, Any]]:
        """根据食堂获取商家列表"""
        query = """
            SELECT id, username, store_name, canteen, location, contact_info, description, status
            FROM merchants 
            WHERE canteen = %s AND status = 'active'
        """
        results = query_all(query, (hall,))
        return [
            {
                "id": result['id'],
                "username": result['username'],
                "storeName": result['store_name'],
                "canteen": result['canteen'],
                "location": result['location'],
                "contact_info": result['contact_info'],
                "description": result['description'],
                "status": result['status']
            }
            for result in results
        ]
    
    def create_merchant(self, merchant_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建商家"""
        query = """
            INSERT INTO merchants (username, store_name, canteen, location, contact_info, description, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'active')
        """
        merchant_id = execute_insert(
            query, 
            (
                merchant_data['username'],
                merchant_data['storeName'],
                merchant_data['canteen'],
                merchant_data.get('location', ''),
                merchant_data.get('contact_info', ''),
                merchant_data.get('description', '')
            )
        )
        
        if merchant_id:
            return {
                "id": merchant_id,
                "username": merchant_data['username'],
                "storeName": merchant_data['storeName'],
                "canteen": merchant_data['canteen']
            }
        return None
    
    def record_traffic(self, traffic_data: Dict[str, Any]) -> Dict[str, Any]:
        """记录客流量"""
        query = """
            INSERT INTO traffic_data (merchant_id, count, waiting_time, timestamp)
            VALUES (%s, %s, %s, %s)
        """
        traffic_id = execute_insert(
            query,
            (
                traffic_data['merchantId'],
                traffic_data['count'],
                traffic_data['waitingTime'],
                traffic_data.get('timestamp', 'NOW()')
            )
        )
        
        if traffic_id:
            return {
                "id": traffic_id,
                "count": traffic_data['count'],
                "waitingTime": traffic_data['waitingTime'],
                "timestamp": traffic_data.get('timestamp', 'NOW()')
            }
        return None
    
    def get_traffic_statistics(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """获取客流量统计"""
        if filters is None:
            filters = {}
        
        # 这里需要根据实际的统计需求来实现
        # 暂时返回空列表
        return []


class DishRepository:
    """菜品数据访问层"""
    
    def search_dishes(self, query: str, filters: Dict[str, Any] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """搜索菜品"""
        if filters is None:
            filters = {}
        
        # 构建搜索条件
        conditions = ["d.status = 'active'"]
        params = []
        
        if query:
            conditions.append("(d.name LIKE %s OR d.description LIKE %s)")
            params.extend([f"%{query}%", f"%{query}%"])
        
        # 添加筛选条件
        if filters.get('category'):
            conditions.append("d.category = %s")
            params.append(filters['category'])
        
        if filters.get('taste'):
            # 处理多个口味（逗号分隔）
            tastes = filters['taste'].split(',') if isinstance(filters['taste'], str) else [filters['taste']]
            if tastes and tastes[0]:  # 确保不是空字符串
                taste_conditions = ' OR '.join(['d.taste = %s'] * len(tastes))
                conditions.append(f"({taste_conditions})")
                params.extend(tastes)
        
        if filters.get('priceMin') is not None:
            conditions.append("d.price >= %s")
            params.append(filters['priceMin'])
        
        if filters.get('priceMax') is not None:
            conditions.append("d.price <= %s")
            params.append(filters['priceMax'])
        
        # 辣度筛选
        if filters.get('spice_level') is not None and filters.get('spice_level') != '':
            conditions.append("d.spice_level <= %s")
            params.append(int(filters['spice_level']))
        
        # 食堂筛选
        if filters.get('hall'):
            conditions.append("m.canteen = %s")
            params.append(filters['hall'])
        
        where_clause = " AND ".join(conditions)
        
        # 获取总数
        count_query = f"""
            SELECT COUNT(*) as total
            FROM dishes d
            WHERE {where_clause}
        """
        total_result = query_one(count_query, tuple(params))
        total = total_result['total'] if total_result else 0
        
        # 分页参数
        page = filters.get('page', 1)
        limit = filters.get('limit', 100)  # 增加默认limit，便于筛选
        offset = (page - 1) * limit
        
        # 获取菜品数据
        query_sql = f"""
            SELECT d.id, d.merchant_id, d.name, d.description, d.price, d.category, 
                   d.taste, d.spice_level, d.image_url, d.is_available, d.stock_quantity, d.rating,
                   m.store_name, m.canteen
            FROM dishes d
            LEFT JOIN merchants m ON d.merchant_id = m.id
            WHERE {where_clause}
            ORDER BY d.rating DESC, d.id DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        dishes = query_all(query_sql, tuple(params))
        
        # 格式化结果
        formatted_dishes = [
            {
                "id": dish['id'],
                "merchant_id": dish['merchant_id'],
                "name": dish['name'],
                "description": dish['description'],
                "price": float(dish['price']),
                "category": dish['category'],
                "taste": dish['taste'],
                "spice_level": dish['spice_level'],
                "image_url": dish['image_url'],
                "is_available": bool(dish['is_available']),
                "stock_quantity": dish['stock_quantity'],
                "rating": float(dish['rating']),
                "store_name": dish['store_name'],
                "merchant_name": dish['store_name'],  # 添加merchant_name字段
                "canteen": dish['canteen']
            }
            for dish in dishes
        ]
        
        pagination = {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
        
        return formatted_dishes, pagination
    
    def filter_dishes(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """筛选菜品"""
        # 使用search_dishes方法进行筛选
        dishes, _ = self.search_dishes("", criteria)
        return dishes
    
    def get_dish_by_id(self, dish_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取菜品"""
        query = """
            SELECT d.id, d.merchant_id, d.name, d.description, d.price, d.category, 
                   d.taste, d.spice_level, d.image_url, d.is_available, d.stock_quantity, d.rating,
                   m.store_name, m.canteen
            FROM dishes d
            LEFT JOIN merchants m ON d.merchant_id = m.id
            WHERE d.id = %s AND d.status = 'active'
        """
        dish = query_one(query, (dish_id,))
        if dish:
            return {
                "id": dish['id'],
                "merchant_id": dish['merchant_id'],
                "name": dish['name'],
                "description": dish['description'],
                "price": float(dish['price']),
                "category": dish['category'],
                "taste": dish['taste'],
                "spice_level": dish['spice_level'],
                "image_url": dish['image_url'],
                "is_available": bool(dish['is_available']),
                "stock_quantity": dish['stock_quantity'],
                "rating": float(dish['rating']),
                "store_name": dish['store_name'],
                "canteen": dish['canteen']
            }
        return None
    
    def get_dishes_by_merchant(self, merchant_id: int) -> List[Dict[str, Any]]:
        """根据商家获取菜品列表"""
        query = """
            SELECT id, merchant_id, name, description, price, category, taste, 
                   spice_level, image_url, is_available, stock_quantity, rating
            FROM dishes 
            WHERE merchant_id = %s AND status = 'active'
            ORDER BY rating DESC, id DESC
        """
        dishes = query_all(query, (merchant_id,))
        return [
            {
                "id": dish['id'],
                "merchant_id": dish['merchant_id'],
                "name": dish['name'],
                "description": dish['description'],
                "price": float(dish['price']),
                "category": dish['category'],
                "taste": dish['taste'],
                "spice_level": dish['spice_level'],
                "image_url": dish['image_url'],
                "is_available": bool(dish['is_available']),
                "stock_quantity": dish['stock_quantity'],
                "rating": float(dish['rating'])
            }
            for dish in dishes
        ]
    
    def create_dish(self, dish_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建菜品"""
        query = """
            INSERT INTO dishes (merchant_id, name, description, price, category, taste, 
                              spice_level, image_url, is_available, stock_quantity, rating, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active')
        """
        dish_id = execute_insert(
            query,
            (
                dish_data['merchantId'],
                dish_data['name'],
                dish_data.get('description', ''),
                dish_data['price'],
                dish_data['category'],
                dish_data['taste'],
                dish_data.get('spice_level', 0),
                dish_data.get('image_url', ''),
                dish_data.get('is_available', True),
                dish_data.get('stock_quantity', 0),
                dish_data.get('rating', 4.0)
            )
        )
        
        if dish_id:
            return {
                "id": dish_id,
                "name": dish_data['name'],
                "price": dish_data['price']
            }
        return None
    
    def update_dish(self, dish_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新菜品"""
        # 构建更新字段
        update_fields = []
        params = []
        
        for field, value in update_data.items():
            if field != 'id' and value is not None:
                update_fields.append(f"{field} = %s")
                params.append(value)
        
        if not update_fields:
            return self.get_dish_by_id(dish_id)
        
        params.append(dish_id)
        query = f"""
            UPDATE dishes 
            SET {', '.join(update_fields)}
            WHERE id = %s AND status = 'active'
        """
        
        affected = execute_update(query, tuple(params))
        if affected > 0:
            return self.get_dish_by_id(dish_id)
        return None
    
    def delete_dish(self, dish_id: int) -> bool:
        """删除菜品（软删除）"""
        query = "UPDATE dishes SET status = 'deleted' WHERE id = %s"
        affected = execute_update(query, (dish_id,))
        return affected > 0
    
    def get_popular_dishes(self) -> List[Dict[str, Any]]:
        """获取热门菜品"""
        query = """
            SELECT d.id, d.merchant_id, d.name, d.description, d.price, d.category, 
                   d.taste, d.spice_level, d.image_url, d.is_available, d.stock_quantity, d.rating,
                   m.store_name, m.canteen
            FROM dishes d
            LEFT JOIN merchants m ON d.merchant_id = m.id
            WHERE d.status = 'active'
            ORDER BY d.rating DESC, d.id DESC
            LIMIT 10
        """
        dishes = query_all(query)
        return [
            {
                "id": dish['id'],
                "merchant_id": dish['merchant_id'],
                "name": dish['name'],
                "description": dish['description'],
                "price": float(dish['price']),
                "category": dish['category'],
                "taste": dish['taste'],
                "spice_level": dish['spice_level'],
                "image_url": dish['image_url'],
                "is_available": bool(dish['is_available']),
                "stock_quantity": dish['stock_quantity'],
                "rating": float(dish['rating']),
                "store_name": dish['store_name'],
                "merchant_name": dish['store_name'],  # 添加merchant_name字段
                "canteen": dish['canteen']
            }
            for dish in dishes
        ]


class OrderRepository:
    """订单数据访问层"""
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建订单"""
        query = """
            INSERT INTO orders (user_id, dish_id, quantity, total_price, status, special_instructions, pickup_time)
            VALUES (%s, %s, %s, %s, 'pending', %s, %s)
        """
        order_id = execute_insert(
            query,
            (
                order_data['userId'],
                order_data['dishId'],
                order_data.get('quantity', 1),
                order_data.get('totalPrice', 0),
                order_data.get('specialInstructions', ''),
                order_data.get('pickupTime', None)
            )
        )
        
        if order_id:
            return {
                "id": order_id,
                "user_id": order_data['userId'],
                "dish_id": order_data['dishId'],
                "status": "pending"
            }
        return None
    
    def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        """获取用户订单列表"""
        query = """
            SELECT o.id, o.user_id, o.dish_id, o.quantity, o.total_price, o.status, 
                   o.special_instructions, o.pickup_time, o.created_at,
                   d.name as dish_name, d.price as dish_price, d.image_url,
                   m.store_name, m.canteen
            FROM orders o
            LEFT JOIN dishes d ON o.dish_id = d.id
            LEFT JOIN merchants m ON d.merchant_id = m.id
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC
        """
        orders = query_all(query, (user_id,))
        return [
            {
                "id": order['id'],
                "user_id": order['user_id'],
                "dish_id": order['dish_id'],
                "quantity": order['quantity'],
                "total_price": float(order['total_price']),
                "status": order['status'],
                "special_instructions": order['special_instructions'],
                "pickup_time": order['pickup_time'],
                "created_at": order['created_at'],
                "dish_name": order['dish_name'],
                "dish_price": float(order['dish_price']),
                "image_url": order['image_url'],
                "store_name": order['store_name'],
                "canteen": order['canteen']
            }
            for order in orders
        ]
    
    def add_favorite(self, user_id: int, dish_id: int) -> Dict[str, Any]:
        """添加收藏"""
        # 检查是否已经收藏
        check_query = "SELECT id FROM favorites WHERE user_id = %s AND dish_id = %s"
        existing = query_one(check_query, (user_id, dish_id))
        
        if existing:
            return existing
        
        query = """
            INSERT INTO favorites (user_id, dish_id)
            VALUES (%s, %s)
        """
        favorite_id = execute_insert(query, (user_id, dish_id))
        
        if favorite_id:
            return {
                "id": favorite_id,
                "user_id": user_id,
                "dish_id": dish_id
            }
        return None
    
    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """获取用户收藏列表"""
        query = """
            SELECT f.id, f.user_id, f.dish_id, f.added_at,
                   d.name as dish_name, d.description, d.price, d.image_url, d.category, d.taste,
                   m.store_name, m.canteen
            FROM favorites f
            LEFT JOIN dishes d ON f.dish_id = d.id
            LEFT JOIN merchants m ON d.merchant_id = m.id
            WHERE f.user_id = %s AND d.status = 'active'
            ORDER BY f.added_at DESC
        """
        favorites = query_all(query, (user_id,))
        return [
            {
                "id": favorite['id'],
                "user_id": favorite['user_id'],
                "dish_id": favorite['dish_id'],
                "added_at": favorite['added_at'],
                "dish_name": favorite['dish_name'],
                "description": favorite['description'],
                "price": float(favorite['price']),
                "image_url": favorite['image_url'],
                "category": favorite['category'],
                "taste": favorite['taste'],
                "store_name": favorite['store_name'],
                "canteen": favorite['canteen']
            }
            for favorite in favorites
        ]
