# API密钥配置指南

## 概述

本项目支持多种LLM提供商，您可以根据需要选择其中一种进行配置。

## 支持的LLM提供商

| 提供商 | 环境变量 | 模型 | 基础URL |
|--------|----------|------|---------|
| OpenAI | `OPENAI_API_KEY` | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` | `https://api.openai.com/v1` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat`, `deepseek-coder` | `https://api.deepseek.com/v1` |
| 智谱AI | `ZHIPU_API_KEY` | `glm-4`, `glm-3-turbo` | `https://open.bigmodel.cn/api/paas/v4` |
| 通义千问 | `DASHSCOPE_API_KEY` | `qwen-turbo`, `qwen-plus`, `qwen-max` | `https://dashscope.aliyuncs.com/api/v1` |
| Azure OpenAI | `AZURE_OPENAI_API_KEY` | `gpt-4`, `gpt-35-turbo` | 需要配置 `AZURE_BASE_URL` |

## 配置方法

### 方法1：环境变量（推荐）

#### Windows PowerShell
```powershell
# 设置DeepSeek API密钥
$env:DEEPSEEK_API_KEY="sk-your_actual_api_key_here"
$env:LLM_PROVIDER="deepseek"
$env:LLM_MODEL="deepseek-chat"

# 或者设置OpenAI
$env:OPENAI_API_KEY="sk-your_openai_api_key"
$env:LLM_PROVIDER="openai"
$env:LLM_MODEL="gpt-3.5-turbo"
```

#### Windows 命令提示符
```cmd
set DEEPSEEK_API_KEY=sk-your_actual_api_key_here
set LLM_PROVIDER=deepseek
set LLM_MODEL=deepseek-chat
```

#### Linux/Mac
```bash
export DEEPSEEK_API_KEY="sk-your_actual_api_key_here"
export LLM_PROVIDER="deepseek"
export LLM_MODEL="deepseek-chat"
```

### 方法2：创建.env文件

在 `canteen_new` 目录下创建 `.env` 文件：

```env
# LLM配置
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# DeepSeek配置
DEEPSEEK_API_KEY=sk-your_actual_api_key_here

# 或者使用OpenAI
# OPENAI_API_KEY=sk-your_openai_api_key

# 其他配置
DEBUG=True
SECRET_KEY=your_django_secret_key
```

### 方法3：系统环境变量

在系统级别设置环境变量：
- `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY`
- `LLM_PROVIDER`
- `LLM_MODEL`

## 获取API密钥

### DeepSeek
1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册账号并登录
3. 进入API密钥管理页面
4. 创建新的API密钥
5. 复制密钥并配置到环境变量

### OpenAI
1. 访问 [OpenAI平台](https://platform.openai.com/)
2. 登录您的账户
3. 进入API密钥页面
4. 创建新的API密钥
5. 复制密钥并配置到环境变量

### 智谱AI
1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册并登录
3. 申请API密钥
4. 配置到环境变量

### 通义千问
1. 访问 [阿里云DashScope](https://dashscope.aliyun.com/)
2. 注册阿里云账号
3. 开通通义千问服务
4. 获取API密钥

## 验证配置

运行以下命令验证配置是否正确：

```bash
cd canteen_new
python config/llm_config.py
```

如果配置正确，您将看到：
```
=== LLM配置信息 ===
提供商: deepseek
模型: deepseek-chat
可用性: 是
配置验证: 通过
====================
```

## 测试完整功能

配置好API密钥后，运行完整测试：

```bash
cd canteen_new
python test_enhanced_ai.py
```

## 故障排除

### 常见问题

1. **API密钥无效**
   - 检查密钥是否正确复制
   - 确保没有多余的空格
   - 验证API密钥是否已激活

2. **网络连接问题**
   - 检查网络连接
   - 确保可以访问API服务端点

3. **配额不足**
   - 检查API使用配额
   - 确认账户余额充足

4. **环境变量未生效**
   - 重启终端或IDE
   - 检查.env文件位置是否正确
   - 验证环境变量名称拼写

### 降级模式

如果API密钥配置不正确或网络不可用，系统会自动降级到模拟模式，仍然可以正常工作，但会使用本地逻辑而非真实LLM。

## 安全建议

1. **不要将API密钥提交到版本控制**
2. **使用.env文件并添加到.gitignore**
3. **定期轮换API密钥**
4. **设置使用限额**

## 示例配置

### 使用DeepSeek的完整配置
```env
# LLM配置
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# DeepSeek API密钥
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Django配置
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///db.sqlite3
```

配置完成后，AI分析功能将使用真实的LLM服务提供智能推荐！
