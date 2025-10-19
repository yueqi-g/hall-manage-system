# 食堂智能管理系统

基于Django + Vue.js的智能食堂管理系统，集成AI推荐功能。

## 系统特性

- **智能菜品推荐**：基于AI的个性化菜品推荐
- **情景感知**：结合天气、节日、客流等数据优化推荐
- **精准筛选**：多维度菜品筛选和搜索
- **响应式设计**：适配各种设备的用户界面

## 技术栈

### 后端
- Django + Django REST Framework
- MySQL 数据库
- 支持多种LLM提供商 (DeepSeek, OpenAI, 智谱AI等)
- 高德天气API集成

### 前端
- Vue.js 3
- Vue Router
- Vuex 状态管理
- Element Plus UI组件库

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+
- Node.js 14+

### 1. 后端配置

#### 安装依赖
```bash
cd canteen_new
pip install django djangorestframework django-cors-headers
pip install openai requests lunarcalendar holidays python-dotenv
```

#### 数据库配置
在MySQL中创建数据库，数据库配置通过环境变量管理。

#### 环境变量配置
复制环境变量模板并配置：

```bash
# 复制模板文件
cp .env.example .env

# 编辑 .env 文件，填入您的API密钥
```

注意需要在在VSCode中启用 `python.terminal.useEnvFile` 设置来自动加载.env文件
2. 或者手动设置环境变量：
   ```bash
   # Windows PowerShell
   $env:LLM_PROVIDER="deepseek"
   $env:LLM_MODEL="deepseek-chat"
   $env:DEEPSEEK_API_KEY="您的API密钥"

   $env:WEATHER_API_KEY="您的API密钥"
   $env:WEATHER_API_PROVIDER="gaode"
   $env:WEATHER_CITY="上海"
   $env:DB_NAME="数据库名"
   $env:DB_PASSWORD="password"
   ```
#### 数据库迁移和启动
```bash
cd canteen_new
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 2. 前端配置
```
# 安装依赖
cd canteen_frontend
npm install

# 启动开发服务器
npm run serve
```