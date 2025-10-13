# 美食食堂终端系统 API 接口表

## 概述
本文档定义了美食食堂终端系统的所有API接口规范，包括请求方法、URL、参数、响应格式和详细的JSON结构体。

## 通用响应格式

```json
{
  "success": "boolean, 请求是否成功",
  "data": "object, 响应数据",
  "message": "string, 响应消息",
  "error": {
    "code": "string, 错误码",
    "details": "string, 错误详情"
  },
  "pagination": {
    "page": "number, 当前页码",
    "limit": "number, 每页数量",
    "total": "number, 总记录数",
    "pages": "number, 总页数"
  }
}
```

## 认证相关 API

### 1. 用户登录
| 项目 | 说明 |
|------|------|
| **接口名称** | 用户登录 |
| **请求方法** | POST |
| **接口地址** | `/api/auth/user/login` |
| **请求头** | `Content-Type: application/json` |
| **使用场景** | LoginModal组件 - 用户登录 |

**请求体 JSON 结构：**
```json
{
  "username": "string, 必填, 用户名",
  "password": "string, 必填, 密码",
  "captcha": "string, 必填, 验证码"
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "number, 用户ID",
      "username": "string, 用户名",
      "email": "string, 邮箱",
      "type": "user, 用户类型",
      "avatar": "string, 头像URL"
    },
    "token": "string, JWT令牌"
  },
  "message": "登录成功"
}
```

### 2. 商家登录
| 项目 | 说明 |
|------|------|
| **接口名称** | 商家登录 |
| **请求方法** | POST |
| **接口地址** | `/api/auth/merchant/login` |
| **请求头** | `Content-Type: application/json` |
| **使用场景** | LoginModal组件 - 商家登录 |

**请求体 JSON 结构：**
```json
{
  "username": "string, 必填, 商家账号",
  "password": "string, 必填, 密码",
  "captcha": "string, 必填, 验证码"
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "merchant": {
      "id": "number, 商家ID",
      "username": "string, 商家账号",
      "storeName": "string, 店铺名称",
      "type": "merchant, 用户类型",
      "canteen": "string, 所属食堂"
    },
    "token": "string, JWT令牌"
  },
  "message": "商家登录成功"
}
```

### 3. 用户注册
| 项目 | 说明 |
|------|------|
| **接口名称** | 用户注册 |
| **请求方法** | POST |
| **接口地址** | `/api/auth/register` |
| **请求头** | `Content-Type: application/json` |
| **使用场景** | LoginModal组件 - 注册账号 |

**请求体 JSON 结构：**
```json
{
  "type": "string, 必填, 注册类型 (user|merchant)",
  "username": "string, 必填, 用户名",
  "password": "string, 必填, 密码",
  "confirmPassword": "string, 必填, 确认密码",
  "email": "string, 必填, 邮箱",
  "storeName": "string, 可选, 商家必填-店铺名称",
  "canteen": "string, 可选, 商家必填-所属食堂"
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "id": "number, 用户ID",
    "username": "string, 用户名"
  },
  "message": "注册成功"
}
```

### 4. 验证码获取
| 项目 | 说明 |
|------|------|
| **接口名称** | 验证码获取 |
| **请求方法** | GET |
| **接口地址** | `/api/auth/captcha` |
| **使用场景** | LoginModal组件 - 验证码生成 |

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "captchaCode": "string, 验证码文本",
    "captchaImage": "string, base64编码的验证码图片"
  }
}
```

## 用户相关 API

### 5. 用户信息
| 项目 | 说明 |
|------|------|
| **接口名称** | 用户信息 |
| **请求方法** | GET |
| **接口地址** | `/api/user/profile` |
| **请求头** | `Authorization: Bearer {token}` |
| **使用场景** | Header组件 - 登录状态检查 |

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "id": "number, 用户ID",
    "username": "string, 用户名",
    "email": "string, 邮箱",
    "avatar": "string, 头像URL",
    "preferences": {
      "favoriteFlavors": ["string", "口味偏好"],
      "budgetRange": {
        "min": "number, 最低预算",
        "max": "number, 最高预算"
      },
      "dietaryRestrictions": ["string", "饮食限制"]
    }
  }
}
```

### 6. 用户收藏
| 项目 | 说明 |
|------|------|
| **接口名称** | 用户收藏列表 |
| **请求方法** | GET |
| **接口地址** | `/api/user/favorites` |
| **请求头** | `Authorization: Bearer {token}` |
| **使用场景** | Header组件 - 我的收藏 |

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "favorites": [
      {
        "id": "number, 收藏ID",
        "dishId": "number, 菜品ID",
        "dishName": "string, 菜品名称",
        "price": "number, 价格",
        "canteen": "string, 所属食堂",
        "addedAt": "string, 收藏时间 (ISO格式)"
      }
    ]
  }
}
```

## 菜品相关 API

### 7. 菜品搜索
| 项目 | 说明 |
|------|------|
| **接口名称** | 菜品搜索 |
| **请求方法** | GET |
| **接口地址** | `/api/dishes/search?q={query}&page={page}&limit={limit}` |
| **使用场景** | UserDashboard组件 - 智能搜索 |

**查询参数：**
- `q`: string, 搜索关键词
- `page`: number, 页码 (默认1)
- `limit`: number, 每页数量 (默认10)

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "dishes": [
      {
        "id": "number, 菜品ID",
        "name": "string, 菜品名称",
        "price": "number, 价格",
        "rating": "number, 评分 (0-5)",
        "description": "string, 菜品描述",
        "canteen": "string, 所属食堂",
        "waitTime": "string, 等待时间",
        "tags": ["string", "标签"],
        "image": "string, 图片URL",
        "category": "string, 品类",
        "taste": "string, 口味",
        "isFavorite": "boolean, 是否已收藏"
      }
    ]
  },
  "pagination": {
    "page": "number, 当前页码",
    "limit": "number, 每页数量",
    "total": "number, 总记录数",
    "pages": "number, 总页数"
  }
}
```

### 8. 菜品筛选
| 项目 | 说明 |
|------|------|
| **接口名称** | 菜品筛选 |
| **请求方法** | GET |
| **接口地址** | `/api/dishes/filter?category={category}&flavors={flavors}&priceMin={min}&priceMax={max}&crowd={crowd}` |
| **使用场景** | UserDashboard组件 - 精确筛选 |

**查询参数：**
- `category`: string, 品类筛选
- `flavors`: string[], 口味筛选 (可多个)
- `priceMin`: number, 最低价格
- `priceMax`: number, 最高价格
- `crowd`: string, 人流量 (low|medium|high|any)

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "dishes": "Array<Dish>, 菜品列表",
    "filters": {
      "category": "string, 筛选品类",
      "flavors": ["string", "筛选口味"],
      "priceRange": {
        "min": "number, 价格下限",
        "max": "number, 价格上限"
      },
      "crowd": "string, 人流量筛选"
    }
  }
}
```

### 9. AI智能推荐
| 项目 | 说明 |
|------|------|
| **接口名称** | AI智能推荐 |
| **请求方法** | POST |
| **接口地址** | `/api/dishes/ai-recommend` |
| **请求头** | `Content-Type: application/json` |
| **使用场景** | UserDashboard组件 - AI助手对话 |

**请求体 JSON 结构：**
```json
{
  "query": "string, 必填, 用户查询文本",
  "preferences": {
    "flavors": ["string", "口味偏好"],
    "budget": {
      "min": "number, 最低预算",
      "max": "number, 最高预算"
    },
    "dietary": ["string", "饮食限制"]
  }
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "dish": "Dish对象, 推荐菜品",
        "reason": "string, 推荐理由",
        "matchScore": "number, 匹配度 (0-1)"
      }
    ],
    "queryAnalysis": {
      "intent": "string, 查询意图",
      "extractedPreferences": {
        "flavors": ["string", "提取的口味"],
        "budget": {
          "min": "number, 提取的最低预算",
          "max": "number, 提取的最高预算"
        },
        "category": "string, 提取的品类"
      }
    }
  }
}
```

### 10. 热门推荐
| 项目 | 说明 |
|------|------|
| **接口名称** | 热门推荐 |
| **请求方法** | GET |
| **接口地址** | `/api/dishes/popular` |
| **使用场景** | UserDashboard组件 - 今日热门推荐 |

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "dishes": [
      {
        "id": "number, 菜品ID",
        "name": "string, 菜品名称",
        "price": "number, 价格",
        "rating": "number, 评分",
        "description": "string, 描述",
        "canteen": "string, 食堂",
        "waitTime": "string, 等待时间",
        "tags": ["string", "标签"],
        "color": "string, 背景颜色",
        "icon": "string, 图标类名"
      }
    ]
  }
}
```

## 订单相关 API

### 11. 下单菜品
| 项目 | 说明 |
|------|------|
| **接口名称** | 下单菜品 |
| **请求方法** | POST |
| **接口地址** | `/api/orders/create` |
| **请求头** | `Authorization: Bearer {token}, Content-Type: application/json` |
| **使用场景** | UserDashboard组件 - 立即下单 |

**请求体 JSON 结构：**
```json
{
  "dishId": "number, 必填, 菜品ID",
  "quantity": "number, 可选, 数量 (默认1)",
  "specialInstructions": "string, 可选, 特殊要求",
  "pickupTime": "string, 可选, 取餐时间 (ISO格式)"
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "orderId": "number, 订单ID",
    "status": "pending, 订单状态",
    "estimatedWaitTime": "number, 预计等待时间(分钟)",
    "totalPrice": "number, 总价格"
  },
  "message": "下单成功"
}
```

### 12. 收藏菜品
| 项目 | 说明 |
|------|------|
| **接口名称** | 收藏菜品 |
| **请求方法** | POST |
| **接口地址** | `/api/favorites/add` |
| **请求头** | `Authorization: Bearer {token}, Content-Type: application/json` |
| **使用场景** | UserDashboard组件 - 收藏菜品 |

**请求体 JSON 结构：**
```json
{
  "dishId": "number, 必填, 菜品ID"
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "favoriteId": "number, 收藏ID"
  },
  "message": "收藏成功"
}
```

## 商家管理 API

### 13. 菜品列表
| 项目 | 说明 |
|------|------|
| **接口名称** | 商家菜品列表 |
| **请求方法** | GET |
| **接口地址** | `/api/merchant/dishes` |
| **请求头** | `Authorization: Bearer {token}` |
| **使用场景** | MerchantDashboard组件 - 菜品管理 |

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "dishes": [
      {
        "id": "number, 菜品ID",
        "name": "string, 菜品名称",
        "price": "number, 价格",
        "category": "string, 品类",
        "taste": "string, 口味",
        "description": "string, 描述",
        "status": "active|inactive, 状态",
        "createdAt": "string, 创建时间",
        "updatedAt": "string, 更新时间"
      }
    ]
  }
}
```

### 14. 添加菜品
| 项目 | 说明 |
|------|------|
| **接口名称** | 添加菜品 |
| **请求方法** | POST |
| **接口地址** | `/api/merchant/dishes` |
| **请求头** | `Authorization: Bearer {token}, Content-Type: application/json` |
| **使用场景** | MerchantDashboard组件 - 添加菜品 |

**请求体 JSON 结构：**
```json
{
  "name": "string, 必填, 菜品名称",
  "price": "number, 必填, 价格",
  "category": "string, 必填, 品类",
  "taste": "string, 必填, 口味",
  "description": "string, 可选, 描述",
  "image": "string, 可选, base64编码的图片"
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "id": "number, 菜品ID",
    "name": "string, 菜品名称",
    "price": "number, 价格"
  },
  "message": "菜品添加成功"
}
```

### 15. 更新菜品
| 项目 | 说明 |
|------|------|
| **接口名称** | 更新菜品 |
| **请求方法** | PUT |
| **接口地址** | `/api/merchant/dishes/{id}` |
| **请求头** | `Authorization: Bearer {token}, Content-Type: application/json` |
| **使用场景** | MerchantDashboard组件 - 编辑菜品 |

**请求体 JSON 结构：**
```json
{
  "name": "string, 可选, 菜品名称",
  "price": "number, 可选, 价格",
  "category": "string, 可选, 品类",
  "taste": "string, 可选, 口味",
  "description": "string, 可选, 描述",
  "image": "string, 可选, base64编码的图片",
  "status": "active|inactive, 可选, 状态"
}
```

### 16. 删除菜品
| 项目 | 说明 |
|------|------|
| **接口名称** | 删除菜品 |
| **请求方法** | DELETE |
| **接口地址** | `/api/merchant/dishes/{id}` |
| **请求头** | `Authorization: Bearer {token}` |
| **使用场景** | MerchantDashboard组件 - 删除菜品 |

**响应体 JSON 结构：**
```json
{
  "success": true,
  "message": "菜品删除成功"
}
```

### 17. 客流量上报
| 项目 | 说明 |
|------|------|
| **接口名称** | 客流量上报 |
| **请求方法** | POST |
| **接口地址** | `/api/merchant/traffic` |
| **请求头** | `Authorization: Bearer {token}, Content-Type: application/json` |
| **使用场景** | MerchantDashboard组件 - 更新客流量 |

**请求体 JSON 结构：**
```json
{
  "count": "number, 必填, 客流量人数",
  "waitingTime": "number, 必填, 平均等待时间(分钟)",
  "timestamp": "string, 可选, 时间戳 (ISO格式)"
}
```

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "trafficId": "number, 上报记录ID",
    "currentTraffic": "number, 当前客流量",
    "avgWaitTime": "number, 平均等待时间",
    "updatedAt": "string, 更新时间"
  },
  "message": "客流量信息更新成功"
}
```

## 数据统计 API

### 18. 实时客流量
| 项目 | 说明 |
|------|------|
| **接口名称** | 实时客流量 |
| **请求方法** | GET |
| **接口地址** | `/api/stats/traffic` |
| **使用场景** | UserDashboard组件 - 人流量筛选 |

**响应体 JSON 结构：**
```json
{
  "success": true,
  "data": {
    "trafficData": [
      {
        "canteen": "string, 食堂名称",
        "currentTraffic": "number, 当前客流量",
        "avgWaitTime": "number, 平均等待时间",
        "level": "low|medium|high, 拥挤程度",
        "lastUpdated": "string, 最后更新时间"
      }
    ]
  }
}
```

## 错误码规范

| 错误码 | 说明 | HTTP状态码 |
|--------|------|------------|
| `AUTH_001` | 认证失败 | 401 |
| `AUTH_002` | Token过期 | 401 |
| `AUTH_003` | 权限不足 | 403 |
| `VALIDATION_001` | 参数验证失败 | 400 |
| `NOT_FOUND_001` | 资源不存在 | 404 |
| `BUSINESS_001` | 业务逻辑错误 | 422 |
| `SERVER_001` | 服务器内部错误 | 500 |

## 使用说明

1. **认证接口**：所有需要认证的接口必须在请求头中包含 `Authorization: Bearer {token}`
2. **分页接口**：支持分页的接口使用 `page` 和 `limit` 参数
3. **错误处理**：所有接口返回统一的错误格式，前端需要根据 `success` 字段判断请求状态
4. **数据验证**：前端应在发送请求前进行基本的数据验证

## 接口调用示例

### 用户登录示例
```javascript
// 请求
fetch('/api/auth/user/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'testuser',
    password: 'password123',
    captcha: 'ABCD'
  })
})

// 响应处理
.then(response => response.json())
.then(data => {
  if (data.success) {
    localStorage.setItem('token', data.data.token)
    localStorage.setItem('user', JSON.stringify(data.data.user))
  } else {
    console.error('登录失败:', data.error.details)
  }
})
```

### 菜品搜索示例
```javascript
// 请求
fetch('/api/dishes/search?q=麻辣香锅&page=1&limit=10')

// 响应处理
.then(response => response.json())
.then(data => {
  if (data.success) {
    const dishes = data.data.dishes
    const pagination = data.pagination
    // 更新界面显示
  }
})
```

这个API接口表为前端开发提供了完整的接口规范，包括详细的JSON结构体定义，便于前后端协作开发。
