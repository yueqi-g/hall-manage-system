# 食堂管理系统 API 接口文档

## 概述

本文档详细描述了食堂管理系统的所有 RESTful API 接口，包括认证、菜品管理、收藏、商家管理和用户管理等模块。

## 基础信息

- **基础URL**: `http://localhost:8000/api/`
- **认证方式**: JWT Token（部分接口需要认证）
- **响应格式**: JSON
- **编码**: UTF-8

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "message": "操作成功",
  "data": {
    // 具体数据
  },
  "timestamp": "2025-10-29T23:35:37Z"
}
```

### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_001",
    "message": "用户名和密码不能为空",
    "details": "用户名和密码不能为空"
  },
  "timestamp": "2025-10-29T23:35:37Z"
}
```

## 1. 认证模块 (Authentication)

### 1.1 用户登录
- **URL**: `/api/auth/user-login/`
- **方法**: `POST`
- **描述**: 用户账号密码登录

**请求参数**:
```json
{
  "username": "string, 必填, 用户名",
  "password": "string, 必填, 密码"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "登录成功",
  "data": {
    "token": "jwt_token_string",
    "user": {
      "id": 1,
      "username": "user123",
      "email": "user@example.com",
      "type": "user"
    }
  }
}
```

### 1.2 商家登录
- **URL**: `/api/auth/merchant-login/`
- **方法**: `POST`
- **描述**: 商家账号密码登录

**请求参数**:
```json
{
  "username": "string, 必填, 商家用户名",
  "password": "string, 必填, 密码"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "商家登录成功",
  "data": {
    "token": "jwt_token_string",
    "merchant": {
      "id": 1,
      "username": "merchant123",
      "storeName": "川菜馆",
      "canteen": "第一食堂"
    }
  }
}
```

### 1.3 用户注册
- **URL**: `/api/auth/register/`
- **方法**: `POST`
- **描述**: 用户注册，支持普通用户和商家注册

**请求参数**:
```json
{
  "type": "string, 必填, 用户类型(user/merchant)",
  "username": "string, 必填, 用户名",
  "password": "string, 必填, 密码",
  "confirmPassword": "string, 必填, 确认密码",
  "email": "string, 必填, 邮箱",
  "storeName": "string, 可选, 商家店铺名称(type=merchant时必填)",
  "canteen": "string, 可选, 所属食堂(type=merchant时必填)"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "type": "user"
  }
}
```

## 2. 菜品模块 (Dishes)

### 2.1 菜品搜索 `GET /api/dishes/search/`
**查询参数**:
- `q`: string, 可选, 搜索关键词
- `page`: int, 可选, 页码，默认1
- `limit`: int, 可选, 每页数量，默认10
- `ordering`: string, 可选, 排序方式(default/price_asc/price_desc)
- `price_min`: float, 可选, 最低价格
- `price_max`: float, 可选, 最高价格
- `spice_level`: string, 可选, 辣度等级
- `crowd_level`: string, 可选, 人流量等级
- `hall`: string, 可选, 食堂名称

**响应结构**:
```json
{
  "success": true,
  "message": "搜索成功",
  "data": {
    "dishes": [
      {
        "id": id,
        "name": "name",
        "description": "desc",
        "price": price,
        "category": "",
        "taste": "",
        "spice_level": ,
        "merchant_name": "",
        "hall": "",
        "image_url": ""
      }
    ],
    "total": 50,
    "page": 1,
    "limit": 10,
    "total_pages": 5
  }
}
```

### 2.2 搜索建议
- **URL**: `/api/dishes/suggestions/`
- **方法**: `GET`
- **描述**: 获取搜索关键词的自动补全建议

**查询参数**:
- `q`: string, 必填, 搜索关键词（至少2个字符）

**响应示例**:
```json
{
  "success": true,
  "message": "获取搜索建议成功",
  "data": [
    "宫保鸡丁",
    "宫保虾球",
    "宫保豆腐"
  ]
}
```

### 2.3 菜品筛选
- **URL**: `/api/dishes/filter/`
- **方法**: `GET`
- **描述**: 多条件筛选菜品

**查询参数**:
- `category`: string, 可选, 菜品分类
- `tastes`: string, 可选, 口味
- `price_min`: float, 可选, 最低价格
- `price_max`: float, 可选, 最高价格
- `spice_level`: string, 可选, 辣度等级
- `crowd_level`: string, 可选, 人流量等级
- `hall`: string, 可选, 食堂名称
- `ordering`: string, 可选, 排序方式

**响应示例**:
```json
{
  "success": true,
  "message": "筛选成功",
  "data": {
    "dishes": [
      {
        "id": 1,
        "name": "宫保鸡丁",
        "price": 25.0,
        "category": "川菜",
        "taste": "麻辣",
        "spice_level": 3,
        "merchant_name": "川菜馆",
        "hall": "第一食堂"
      }
    ],
    "total": 15
  }
}
```

### 2.4 热门推荐
- **URL**: `/api/dishes/popular/`
- **方法**: `GET`
- **描述**: 获取热门菜品列表

**响应示例**:
```json
{
  "success": true,
  "message": "获取热门菜品成功",
  "data": {
    "dishes": [
      {
        "id": 1,
        "name": "宫保鸡丁",
        "price": 25.0,
        "popularity": 95,
        "merchant_name": "川菜馆"
      }
    ]
  }
}
```

### 2.5 AI智能推荐
- **URL**: `/api/dishes/ai-recommend/`
- **方法**: `POST`
- **描述**: 基于用户查询和偏好的AI菜品推荐

**请求参数**:
```json
{
  "query": "string, 必填, 用户查询内容",
  "preferences": {
    "taste": "string, 可选, 口味偏好",
    "spice_level": "int, 可选, 辣度偏好",
    "price_range": "array, 可选, 价格范围"
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "AI推荐成功",
  "data": {
    "recommended_dishes": [
      {
        "id": 1,
        "name": "宫保鸡丁",
        "reason": "符合您的麻辣口味偏好",
        "match_score": 0.95
      }
    ],
    "processing_mode": "context_aware",
    "context_aware": true,
    "user_preferences_used": true
  }
}
```

### 2.6 菜品详情
- **URL**: `/api/dishes/{id}/`
- **方法**: `GET`
- **描述**: 获取指定菜品的详细信息

**路径参数**:
- `id`: int, 必填, 菜品ID

**响应示例**:
```json
{
  "success": true,
  "message": "获取菜品详情成功",
  "data": {
    "id": 1,
    "name": "宫保鸡丁",
    "description": "经典川菜，鸡肉鲜嫩，花生香脆",
    "price": 25.0,
    "category": "川菜",
    "taste": "麻辣",
    "spice_level": 3,
    "merchant_id": 1,
    "merchant_name": "川菜馆",
    "hall": "第一食堂",
    "image_url": "http://example.com/image.jpg",
    "is_available": true,
    "stock_quantity": 50,
    "created_at": "2025-10-29T10:00:00Z",
    "updated_at": "2025-10-29T10:00:00Z"
  }
}
```

## 3. 收藏模块 (Favorites)

### 3.1 添加收藏
- **URL**: `/api/favorites/add/`
- **方法**: `POST`
- **描述**: 用户收藏菜品

**请求参数**:
```json
{
  "dishId": "int, 必填, 菜品ID",
  "userId": "int, 必填, 用户ID"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "收藏成功",
  "data": {
    "favoriteId": 1,
    "dishId": 1,
    "message": "收藏成功"
  }
}
```

### 3.2 获取收藏列表
- **URL**: `/api/favorites/`
- **方法**: `GET`
- **描述**: 获取用户的所有收藏菜品

**查询参数**:
- `userId`: int, 必填, 用户ID

**响应示例**:
```json
{
  "success": true,
  "message": "获取收藏列表成功",
  "data": {
    "favorites": [
      {
        "id": 1,
        "dish_id": 1,
        "dish_name": "宫保鸡丁",
        "dish_price": 25.0,
        "merchant_name": "川菜馆",
        "added_at": "2025-10-29T10:00:00Z"
      }
    ],
    "total": 5
  }
}
```

### 3.3 移除收藏
- **URL**: `/api/favorites/{id}/`
- **方法**: `DELETE`
- **描述**: 用户取消收藏

**路径参数**:
- `id`: int, 必填, 收藏记录ID

**查询参数**:
- `userId`: int, 必填, 用户ID

**响应示例**:
```json
{
  "success": true,
  "message": "取消收藏成功",
  "data": {
    "message": "取消收藏成功"
  }
}
```

## 4. 商家管理模块 (Merchant)

### 4.1 商家菜品列表
- **URL**: `/api/merchants/dishes/`
- **方法**: `GET`
- **描述**: 获取指定商家的所有菜品

**查询参数**:
- `merchant`: int, 必填, 商家ID

**响应示例**:
```json
{
  "success": true,
  "message": "获取菜品列表成功",
  "data": {
    "dishes": [
      {
        "id": 1,
        "name": "宫保鸡丁",
        "price": 25.0,
        "category": "川菜",
        "is_available": true,
        "stock_quantity": 50
      }
    ]
  }
}
```

### 4.2 添加菜品
- **URL**: `/api/merchants/dishes/add/`
- **方法**: `POST`
- **描述**: 商家添加新菜品

**请求参数**:
```json
{
  "merchant": "int, 必填, 商家ID",
  "name": "string, 必填, 菜品名称",
  "description": "string, 可选, 菜品描述",
  "price": "float, 必填, 价格",
  "category": "string, 必填, 菜品分类",
  "taste": "string, 必填, 口味",
  "spice_level": "int, 可选, 辣度等级(0-5)",
  "image_url": "string, 可选, 图片URL",
  "is_available": "boolean, 可选, 是否可用",
  "stock_quantity": "int, 可选, 库存数量"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "菜品添加成功",
  "data": {
    "id": 1,
    "name": "宫保鸡丁",
    "price": 25.0,
    "category": "川菜"
  }
}
```

### 4.3 更新菜品
- **URL**: `/api/merchants/dishes/{id}/`
- **方法**: `PUT`
- **描述**: 商家更新菜品信息

**路径参数**:
- `id`: int, 必填, 菜品ID

**请求参数**:
```json
{
  "merchant_id": "int, 必填, 商家ID",
  "name": "string, 可选, 菜品名称",
  "description": "string, 可选, 菜品描述",
  "price": "float, 可选, 价格",
  "category": "string, 可选, 菜品分类",
  "taste": "string, 可选, 口味",
  "spice_level": "int, 可选, 辣度等级",
  "image_url": "string, 可选, 图片URL",
  "is_available": "boolean, 可选, 是否可用",
  "stock_quantity": "int, 可选, 库存数量"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "菜品更新成功",
  "data": {
    "id": 1,
    "name": "宫保鸡丁(更新)",
    "price": 28.0
  }
}
```

### 4.4 删除菜品
- **URL**: `/api/merchants/dishes/{id}/delete/`
- **方法**: `DELETE`
- **描述**: 商家删除菜品

**路径参数**:
- `id`: int, 必填, 菜品ID

**请求参数**:
- `merchant_id`: int, 必填, 商家ID（可通过请求体或查询参数传递）

**响应示例**:
```json
{
  "success": true,
  "message": "菜品删除成功",
  "data": {
    "id": 1,
    "message": "菜品已删除"
  }
}
```

### 4.5 客流量上报
- **URL**: `/api/merchants/traffic/`
- **方法**: `POST`
- **描述**: 商家上报当前客流量和等待时间

**请求参数**:
```json
{
  "merchant_id": "int, 必填, 商家ID",
  "count": "int, 必填, 客流量人数",
  "waitingTime": "float, 必填, 等待时间(分钟)",
  "timestamp": "string, 可选, 时间戳"
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "客流量信息更新成功",
  "data": {
    "merchant_id": 1,
    "count": 25,
    "waiting_time": 8.5,
    "crowd_level": "中等",
    "updated_at": "2025-10-29T10:00:00Z"
  }
}
```

### 4.6 商家列表查询
- **URL**: `/api/merchants/`
- **方法**: `GET`
- **描述**: 按用户名搜索商家或按食堂筛选商家

**查询参数**:
- `search`: string, 可选, 商家用户名搜索
- `hall`: string, 可选, 食堂名称筛选

**响应示例**:
```json
{
  "success": true,
  "message": "查询成功",
  "data": {
    "results": [
      {
        "id": 1,
        "username": "merchant123",
        "storeName": "川菜馆",
        "canteen": "第一食堂"
      }
    ],
    "count": 1
  }
}
```

## 5. 用户管理模块 (User)

### 5.1 获取用户信息
- **URL**: `/api/user/profile/`
- **方法**: `GET`
- **描述**: 获取当前登录用户的个人信息（需要认证）

**响应示例**:
```json
{
  "success": true,
  "message": "获取用户信息成功",
  "data": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "type": "user",
    "created_at": "2025-10-29T10:00:00Z"
  }
}
```

### 5.2 用户偏好设置
- **URL**: `/api/user/preferences/`
- **方法**: `GET/PUT`
- **描述**: 获取和更新用户的偏好设置

#### GET - 获取用户偏好设置
**查询参数**:
- `userId`: int, 必填, 用户ID

**响应示例**:
```json
{
  "success": true,
  "message": "获取用户偏好成功",
  "data": {
    "taste": "麻辣",
    "spice_level": 3,
    "price_range": [15, 30],
    "preferred_categories": ["川菜", "湘菜"],
    "avoid_ingredients": ["香菜", "花生"]
  }
}
```

#### PUT - 更新用户偏好设置
**请求参数**:
```json
{
  "userId": "int, 必填, 用户ID",
  "preferences": {
    "taste": "string, 可选, 口味偏好",
    "spice_level": "int, 可选, 辣度偏好(0-5)",
    "price_range": "array, 可选, 价格范围[min, max]",
    "preferred_categories": "array, 可选, 偏好的菜品分类",
    "avoid_ingredients": "array, 可选, 避免的食材"
  }
}
```

**响应示例**:
```json
{
  "success": true,
  "message": "更新用户偏好成功",
  "data": {
    "userId": 1,
    "preferences": {
      "taste": "麻辣",
      "spice_level": 3,
      "price_range": [15, 30]
    }
  }
}
```

## 6. 错误代码说明

### 6.1 通用错误代码
- `SERVER_001`: 服务器内部错误
- `VALIDATION_001`: 参数验证失败
- `AUTH_001`: 认证失败
- `NOT_FOUND_001`: 资源不存在

### 6.2 业务错误代码
- `DISH_001`: 菜品不存在
- `FAV_001`: 收藏失败
- `FAV_002`: 取消收藏失败
- `USER_001`: 用户操作失败
- `BUSINESS_001`: 业务逻辑错误
- `DUPLICATE_DISH`: 重复菜品名称

## 7. 接口使用说明

### 7.1 认证流程
1. 用户/商家通过登录接口获取token
2. 在后续请求的Header中添加: `Authorization: Bearer {token}`
3. 需要认证的接口会自动验证token有效性

### 7.2 分页说明
- 所有列表接口都支持分页
- 默认页码: 1
- 默认每页数量: 10
- 响应中包含分页信息: `total`, `page`, `limit`, `total_pages`

### 7.3 筛选条件
- 支持多条件组合筛选
- 空值参数会被忽略
- 支持价格范围、分类、口味、辣度、人流量等筛选

### 7.4 AI推荐
- 基于用户查询内容和历史偏好
- 支持上下文感知
- 返回推荐理由和匹配度

## 8. 注意事项

1. 所有时间戳使用ISO 8601格式
2. 价格单位为元，保留两位小数
3. 图片URL支持相对路径和绝对路径
4. 字符串参数建议进行URL编码
5. 批量操作建议使用分页，避免数据量过大

## 9. 版本信息

- **当前版本**: v1.0
- **更新日期**: 2025-10-29
- **维护者**: 食堂管理系统开发团队

---
*本文档会根据接口变更实时更新，请关注最新版本*
