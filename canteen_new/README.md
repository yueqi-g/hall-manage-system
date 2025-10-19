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

### 3. 测试配置

#### 测试AI模块
```bash
cd test
python test_ai_architecture.py
```

#### 测试天气API
```bash
cd test
python test_weather_api.py
```

#### 测试DeepSeek连接
```bash
cd test
python test_deepseek.py
```

## AI模块架构

系统采用两阶段处理流程：

1. **关键词提取阶段**：从用户输入中提取菜品相关参数
2. **LLM增强阶段**：结合情景数据使用大语言模型优化推荐

### 情景数据集成

- **天气数据**：实时天气条件影响推荐策略
- **节日节气**：传统节日和节气特色菜品推荐
- **客流量**：基于时间段的客流模式分析
- **用户偏好**：个性化口味和预算偏好

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否启动
   - 验证数据库配置信息

2. **API服务不可用**
   - 系统会自动降级到关键词提取模式
   - 检查API密钥配置和网络连接

3. **前端显示异常**
   - 检查后端服务是否正常启动
   - 验证API接口调用

### 降级机制

系统具备完善的降级机制：
- LLM不可用 → 关键词提取模式
- 天气API不可用 → 基于季节的备用数据
- 确保核心功能始终可用

## 开发说明

### 项目结构
```
canteen_new/
├── ai/                    # AI模块
│   ├── orchestrator.py    # 流程编排器
│   ├── keyword_extractor.py
│   ├── llm_service.py
│   └── context_service.py
├── api/                   # API接口
├── config/               # 配置文件
└── data/                 # 数据服务
```

### 扩展开发

#### 添加新的LLM提供商
1. 在 `config/llm_config.py` 中添加提供商配置
2. 更新环境变量支持

#### 添加新的天气提供商
1. 扩展 `ai/context_service.py` 中的 `ContextService` 类
2. 实现新的天气数据获取方法

## 许可证

MIT License
