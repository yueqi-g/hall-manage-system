"""
数据库初始化模块
在启动服务时检查数据库表是否存在，如果不存在，自动创建
"""
import logging
from typing import List
from .database import execute_raw_query, execute_raw_update

logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """数据库初始化类"""
    
    def __init__(self):
        self.required_tables = [
            'users',
            'merchants', 
            'dishes',
            'orders',
            'favorites',
            'traffic_data'
        ]
    
    def check_table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        try:
            query = f"""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_schema = DATABASE() 
                AND table_name = %s
            """
            result = execute_raw_query(query, (table_name,))
            return len(result) > 0 and result[0]['count'] > 0
        except Exception as e:
            logger.error(f"检查表 {table_name} 是否存在时出错: {e}")
            return False
    
    def create_users_table(self) -> bool:
        """创建用户表"""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    type ENUM('user', 'merchant', 'admin') NOT NULL DEFAULT 'user',
                    avatar VARCHAR(255),
                    status ENUM('active', 'inactive', 'deleted') NOT NULL DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_username (username),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_raw_update(query)
            logger.info("用户表创建成功")
            return True
        except Exception as e:
            logger.error(f"创建用户表失败: {e}")
            return False
    
    def create_merchants_table(self) -> bool:
        """创建商家表"""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS merchants (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    store_name VARCHAR(100) NOT NULL,
                    canteen VARCHAR(50) NOT NULL,
                    location VARCHAR(100),
                    contact_info VARCHAR(100),
                    description TEXT,
                    status ENUM('active', 'inactive', 'deleted') NOT NULL DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_username (username),
                    INDEX idx_canteen (canteen),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_raw_update(query)
            logger.info("商家表创建成功")
            return True
        except Exception as e:
            logger.error(f"创建商家表失败: {e}")
            return False
    
    def create_dishes_table(self) -> bool:
        """创建菜品表"""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS dishes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    merchant_id INT NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    taste VARCHAR(50) NOT NULL,
                    spice_level INT DEFAULT 0,
                    image_url VARCHAR(255),
                    is_available BOOLEAN DEFAULT TRUE,
                    stock_quantity INT DEFAULT 0,
                    rating DECIMAL(3,2) DEFAULT 4.0,
                    status ENUM('active', 'inactive', 'deleted') NOT NULL DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_merchant_id (merchant_id),
                    INDEX idx_category (category),
                    INDEX idx_taste (taste),
                    INDEX idx_price (price),
                    INDEX idx_rating (rating),
                    INDEX idx_status (status),
                    UNIQUE KEY unique_merchant_dish (merchant_id, name, status),
                    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_raw_update(query)
            logger.info("菜品表创建成功")
            return True
        except Exception as e:
            logger.error(f"创建菜品表失败: {e}")
            return False
    
    def create_orders_table(self) -> bool:
        """创建订单表"""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    dish_id INT NOT NULL,
                    quantity INT NOT NULL DEFAULT 1,
                    total_price DECIMAL(10,2) NOT NULL,
                    status ENUM('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
                    special_instructions TEXT,
                    pickup_time TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_user_id (user_id),
                    INDEX idx_dish_id (dish_id),
                    INDEX idx_status (status),
                    INDEX idx_created_at (created_at),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_raw_update(query)
            logger.info("订单表创建成功")
            return True
        except Exception as e:
            logger.error(f"创建订单表失败: {e}")
            return False
    
    def create_favorites_table(self) -> bool:
        """创建收藏表"""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS favorites (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    dish_id INT NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_user_dish (user_id, dish_id),
                    INDEX idx_user_id (user_id),
                    INDEX idx_dish_id (dish_id),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_raw_update(query)
            logger.info("收藏表创建成功")
            return True
        except Exception as e:
            logger.error(f"创建收藏表失败: {e}")
            return False
    
    def create_traffic_data_table(self) -> bool:
        """创建客流量数据表"""
        try:
            query = """
                CREATE TABLE IF NOT EXISTS traffic_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    merchant_id INT NOT NULL,
                    count INT NOT NULL,
                    waiting_time INT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_merchant_id (merchant_id),
                    INDEX idx_timestamp (timestamp),
                    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            execute_raw_update(query)
            logger.info("客流量数据表创建成功")
            return True
        except Exception as e:
            logger.error(f"创建客流量数据表失败: {e}")
            return False
    
    def initialize_database(self) -> bool:
        """初始化数据库"""
        logger.info("开始检查数据库表结构...")
        
        # 检查所有必需的表
        missing_tables = []
        for table in self.required_tables:
            if not self.check_table_exists(table):
                missing_tables.append(table)
                logger.warning(f"表 {table} 不存在")
        
        if not missing_tables:
            logger.info("所有必需的表都已存在")
            return True
        
        logger.info(f"需要创建的表: {missing_tables}")
        
        # 创建缺失的表
        creation_results = {}
        
        # 按依赖顺序创建表
        if 'users' in missing_tables:
            creation_results['users'] = self.create_users_table()
        
        if 'merchants' in missing_tables:
            creation_results['merchants'] = self.create_merchants_table()
        
        if 'dishes' in missing_tables:
            creation_results['dishes'] = self.create_dishes_table()
        
        if 'orders' in missing_tables:
            creation_results['orders'] = self.create_orders_table()
        
        if 'favorites' in missing_tables:
            creation_results['favorites'] = self.create_favorites_table()
        
        if 'traffic_data' in missing_tables:
            creation_results['traffic_data'] = self.create_traffic_data_table()
        
        # 检查创建结果
        failed_tables = [table for table, success in creation_results.items() if not success]
        
        if failed_tables:
            logger.error(f"以下表创建失败: {failed_tables}")
            return False
        else:
            logger.info("所有表创建成功")
            return True
    
    def insert_sample_data(self) -> bool:
        """插入示例数据"""
        try:
            # 检查是否需要插入示例数据
            users_count = execute_raw_query("SELECT COUNT(*) as count FROM users")[0]['count']
            if users_count > 0:
                logger.info("数据库中已有数据，跳过示例数据插入")
                return True
            
            logger.info("开始插入示例数据...")
            
            # 插入示例用户数据
            sample_users = [
                ("testuser", "sha256$f47e4d3b78abefa88c0918dd105e2288$2ca067e75246b92b96759239d105b74cf749ad1db4abd0e46f4442aa00f7e1f6", "testuser@example.com", "user"),
                ("merchant1", "sha256$14a68b4d877cf22fddae1d2c9888e451$4cde8fb68e7197876150cf047798e7b875bb6a2af718b8d01cae47967e3fe7bc", "merchant1@example.com", "merchant"),
                ("admin", "sha256$bdef1701a591f259a6cc9b3112743861$8d79dd0970b8ec8f42a0778bcdb6577a8d548be054a0524fd5c974e73050a8b9", "admin@example.com", "admin")
            ]
            
            for username, password, email, user_type in sample_users:
                execute_raw_update(
                    "INSERT INTO users (username, password, email, type) VALUES (%s, %s, %s, %s)",
                    (username, password, email, user_type)
                )
            
            # 插入示例商家数据
            sample_merchants = [
                ("merchant1", "川菜馆", "一食堂", "窗口1", "13800138001", "正宗川菜，麻辣鲜香"),
                ("merchant2", "粤菜馆", "一食堂", "窗口2", "13800138002", "清淡粤菜，营养健康"),
                ("merchant3", "面食馆", "二食堂", "窗口1", "13800138003", "各种面食，手工制作")
            ]
            
            for username, store_name, canteen, location, contact_info, description in sample_merchants:
                execute_raw_update(
                    "INSERT INTO merchants (username, store_name, canteen, location, contact_info, description) VALUES (%s, %s, %s, %s, %s, %s)",
                    (username, store_name, canteen, location, contact_info, description)
                )
            
            logger.info("示例数据插入成功")
            return True
            
        except Exception as e:
            logger.error(f"插入示例数据失败: {e}")
            return False


# 创建全局实例
db_initializer = DatabaseInitializer()


def initialize_database_on_startup():
    """在启动时初始化数据库"""
    return db_initializer.initialize_database()


def insert_sample_data_on_startup():
    """在启动时插入示例数据"""
    return db_initializer.insert_sample_data()
