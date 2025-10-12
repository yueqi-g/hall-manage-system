# 食堂管理系统 - 前后端集成版

这是一个基于Django后端和HTML/CSS/JavaScript前端的食堂管理系统，支持用户和商家两种角色。

## 功能特性

### 用户功能
- 智能菜品推荐
- 多维度筛选（品类、口味、价格、人流量）
- AI美食助手聊天
- 用户登录/注册
- 菜品收藏和下单

### 商家功能
- 菜品管理（添加、编辑、删除）
- 客流量实时更新
- 商家登录/注册
- 数据统计展示

### 系统功能
- 响应式设计
- 实时数据更新
- RESTful API接口
- 用户认证系统

## 技术栈

- **后端**: Django 5.2.6, Django REST Framework
- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **数据库**: SQLite3
- **样式**: 自定义CSS + Font Awesome图标

## 安装和运行

### 1. 环境要求
- Python 3.8+
- pip

### 2. 安装依赖
```bash
cd canteen_system
pip install -r requirements.txt
```

如果没有requirements.txt文件，请安装以下依赖：
```bash
pip install django==5.2.6
pip install djangorestframework
pip install django-cors-headers
```

### 3. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 5. 启动服务器
```bash
# 方法1：使用Django命令
python manage.py runserver

# 方法2：使用启动脚本
python run_server.py
```

### 6. 访问系统
- 主页: http://127.0.0.1:8000/
- 用户仪表板: http://127.0.0.1:8000/user/
- 商家仪表板: http://127.0.0.1:8000/merchant/
- API接口: http://127.0.0.1:8000/api/
- 管理后台: http://127.0.0.1:8000/admin/

## 项目结构

```
canteen_system/
├── canteen/                    # Django应用
│   ├── migrations/            # 数据库迁移文件
│   ├── models.py             # 数据模型
│   ├── views.py              # API视图
│   ├── frontend_views.py     # 前端集成视图
│   ├── serializers.py        # 序列化器
│   ├── urls.py               # URL路由
│   └── ...
├── canteen_system/           # Django项目配置
│   ├── settings.py           # 项目设置
│   ├── urls.py              # 主URL配置
│   └── ...
├── manage.py                 # Django管理脚本
├── run_server.py            # 启动脚本
└── README.md                # 项目说明

../frontend/                 # 前端文件
├── assets/                  # 静态资源
│   ├── css/                # 样式文件
│   └── js/                 # JavaScript文件
├── index.html              # 主页
├── user_dashboard.html     # 用户仪表板
└── merchant_dashboard.html # 商家仪表板
```

## API接口

### 认证接口
- `POST /api/auth/login/` - 用户/商家登录
- `POST /api/auth/login/` - 用户/商家注册

### 商家接口
- `GET /api/merchant/dishes/` - 获取商家菜品列表
- `POST /api/merchant/dishes/` - 添加菜品
- `DELETE /api/merchant/dishes/{id}/` - 删除菜品
- `GET /api/merchant/traffic/` - 获取客流量数据
- `POST /api/merchant/traffic/` - 更新客流量

### 其他接口
- `GET /api/dishes/` - 获取所有菜品
- `GET /api/merchants/` - 获取商家列表
- `POST /api/ai-services/recommend_dishes/` - AI菜品推荐

## 使用说明

### 用户使用
1. 访问主页 http://127.0.0.1:8000/
2. 点击"登录/注册"按钮
3. 选择"用户登录"或"注册账号"
4. 登录后可以浏览菜品、使用AI助手、筛选菜品等

### 商家使用
1. 访问主页 http://127.0.0.1:8000/
2. 点击"登录/注册"按钮
3. 选择"商家登录"或注册商家账号
4. 登录后可以管理菜品、更新客流量等

## 开发说明

### 添加新功能
1. 在`models.py`中定义数据模型
2. 在`views.py`或`frontend_views.py`中创建视图
3. 在`urls.py`中添加路由
4. 在前端JavaScript中添加相应的API调用

### 修改样式
- 修改`frontend/assets/css/`目录下的CSS文件
- 主要样式文件：
  - `style.css` - 通用样式
  - `auth.css` - 认证相关样式
  - `user.css` - 用户页面样式
  - `merchant.css` - 商家页面样式

### 数据库管理
```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 进入Django shell
python manage.py shell

# 访问管理后台
python manage.py runserver
# 然后访问 http://127.0.0.1:8000/admin/
```

## 故障排除

### 常见问题
1. **静态文件无法加载**
   - 确保`STATICFILES_DIRS`配置正确
   - 运行`python manage.py collectstatic`

2. **API请求失败**
   - 检查URL路径是否正确
   - 确保Django服务器正在运行
   - 检查CORS配置

3. **页面显示异常**
   - 检查浏览器控制台错误信息
   - 确保所有静态文件路径正确
   - 检查JavaScript语法错误

## 许可证

本项目仅供学习和演示使用。

## 联系方式

如有问题，请联系开发团队。
