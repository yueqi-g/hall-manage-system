create database hall DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

-- 创建商家表
CREATE TABLE merchants (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '商家编号',
    name VARCHAR(100) NOT NULL COMMENT '商家名称',
    hall VARCHAR(50) NOT NULL COMMENT '食堂号',
    location VARCHAR(50) NOT NULL COMMENT '窗口号',
    contact_info VARCHAR(100) COMMENT '联系方式',
    description TEXT COMMENT '商家描述',
    status TINYINT DEFAULT 1 COMMENT '商家状态：0-关闭，1-营业',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_hall (hall),
    INDEX idx_location (location),
    UNIQUE KEY uk_merchant_location (hall, location)
) COMMENT '商家信息表';

-- 创建菜品表
CREATE TABLE dishes (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '菜品编号',
    merchant_id INT NOT NULL COMMENT '商家ID',
    name VARCHAR(100) NOT NULL COMMENT '菜品名称',
    description TEXT COMMENT '菜品描述',
    price DECIMAL(10,2) NOT NULL COMMENT '价格',
    category ENUM('饭', '面', '饺子', '其他') NOT NULL COMMENT '品类',
    taste ENUM('辣', '咸', '淡', '酸甜') NOT NULL COMMENT '口味',
    spice_level TINYINT DEFAULT 0 COMMENT '辣度等级 0-5',
    image_url VARCHAR(255) COMMENT '菜品图片URL',
    is_available BOOLEAN DEFAULT TRUE COMMENT '是否可用',
    stock_quantity INT DEFAULT 0 COMMENT '库存数量',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE,
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_category (category),
    INDEX idx_taste (taste),
    INDEX idx_price (price),
    INDEX idx_availability (is_available)
) COMMENT '菜品信息表';

-- 创建用户偏好表
CREATE TABLE user_preferences (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户编号',
    user_name VARCHAR(50) NOT NULL COMMENT '用户姓名',
    preferred_categories JSON COMMENT '偏好品类',
    preferred_tastes JSON COMMENT '偏好口味',
    price_range_min DECIMAL(10,2) DEFAULT 0 COMMENT '最低价格',
    price_range_max DECIMAL(10,2) DEFAULT 999.99 COMMENT '最高价格',
    dietary_restrictions JSON COMMENT '饮食限制',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_user_name (user_name)
) COMMENT '用户偏好表';

-- 创建订单表（优化后的结构）
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '订单编号',
    user_id INT NOT NULL COMMENT '用户编号',
    merchant_id INT NOT NULL COMMENT '商家ID',
    total_amount DECIMAL(10,2) NOT NULL COMMENT '订单总金额',
    item_count INT NOT NULL COMMENT '菜品总数',
    status ENUM('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '订单状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    INDEX idx_user_id (user_id),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) COMMENT '订单表';

-- 创建订单项表（解决多对多关系）
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '订单项ID',
    order_id INT NOT NULL COMMENT '订单编号',
    dish_id INT NOT NULL COMMENT '菜品编号',
    quantity INT NOT NULL COMMENT '菜品数量',
    unit_price DECIMAL(10,2) NOT NULL COMMENT '下单时单价',
    subtotal DECIMAL(10,2) NOT NULL COMMENT '小计金额',
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (dish_id) REFERENCES dishes(id),
    INDEX idx_order_id (order_id),
    INDEX idx_dish_id (dish_id)
) COMMENT '订单明细表';

-- 创建客流量表
CREATE TABLE foot_traffic (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '主键',
    merchant_id INT NOT NULL COMMENT '商家ID',
    traffic_count INT NOT NULL COMMENT '客流量',
    record_date DATE NOT NULL COMMENT '记录日期',
    time_slot ENUM('早餐', '午餐', '晚餐') NOT NULL COMMENT '时间段',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录时间',
    
    FOREIGN KEY (merchant_id) REFERENCES merchants(id) ON DELETE CASCADE,
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_record_date (record_date),
    INDEX idx_time_slot (time_slot),
    UNIQUE KEY uk_traffic_record (merchant_id, record_date, time_slot)
) COMMENT '客流量统计表';