# AI模块实现过程文档

## 1. 系统架构分析

### 当前状态
- **数据访问层**: 已实现`DishRepository`类，包含`search_dishes`和`filter_dishes`方法
- **服务层**: `DishService`类已存在，但缺少AI推荐相关方法
- **API层**: `ai_recommend` API接口已定义，但返回空数据

### 需要新增的组件
1. **AI工具函数**: `get_dishes_by_criteria` - 用于AI模型调用的标准化查询函数
2. **工具函数Schema**: 在`canteen_new/ai/utils.py`中定义函数调用规范
3. **AI服务层**: 在`canteen_new/ai/services.py`中实现LLM调用和参数验证
4. **数据服务增强**: 在`canteen_new/data/services.py`中添加AI推荐服务

## 2. 工具函数Schema设计

### 函数定义要求
```python
# canteen_new/ai/utils.py
def get_dishes_by_criteria(
    name: str = None,
    category: str = None,
    taste: str = None,
    min_price: float = None,
    max_price: float = None,
    min_rating: float = None,
    spice_level: int = None,
    sort_by: str = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """根据多种条件查询菜品"""
    # 实现逻辑
```

### Schema定义（符合OpenAI Function Calling规范）
```python
GET_DISHES_SCHEMA = {
    "name": "get_dishes_by_criteria",
    "description": "根据用户需求查询符合条件的菜品",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "菜品名称关键词，支持模糊匹配"
            },
            "category": {
                "type": "string", 
                "description": "菜品分类：饭、面、饺子、其他"
            },
            "taste": {
                "type": "string",
                "description": "口味偏好：辣、咸、淡、酸甜"
            },
            "min_price": {
                "type": "number",
                "description": "最低价格，单位：元"
            },
            "max_price": {
                "type": "number", 
                "description": "最高价格，单位：元"
            },
            "min_rating": {
                "type": "number",
                "description": "最低评分，范围0.0-5.0"
            },
            "spice_level": {
                "type": "integer",
                "description": "辣度级别，整数值0到5，0为不辣，5为特辣"
            },
            "sort_by": {
                "type": "string",
                "description": "排序方式：rating(评分)、price_asc(价格升序)、price_desc(价格降序)、created_at(最新)"
            },
            "limit": {
                "type": "integer", 
                "description": "返回结果数量限制，默认10，最大50"
            }
        },
        "required": []  # 所有参数均为可选
    }
}
```

## 3. LLM API调用参数设置

### 调用配置
```python
# canteen_new/ai/services.py
LLM_CONFIG = {
    "temperature": 0.0,      # 确保输出确定性
    "top_p": 0.1,           # 限制采样空间
    "max_tokens": 1000,     # 限制响应长度
    "tools": [GET_DISHES_SCHEMA],  # 可用的工具函数
    "tool_choice": "auto"   # 让模型自行决定是否调用工具
}
```

### 调用逻辑
```python
def call_llm_for_recommendation(user_query: str, user_preferences: Dict = None):
    """调用LLM进行智能推荐"""
    messages = [
        {
            "role": "system",
            "content": """你是一个食堂菜品推荐助手。根据用户需求，调用合适的工具函数查询菜品。
            如果用户需求明确涉及菜品查询，调用get_dishes_by_criteria函数。
            如果只是闲聊或非菜品相关查询，直接回复而不调用工具。"""
        },
        {
            "role": "user", 
            "content": user_query
        }
    ]
    
    # 调用LLM API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        **LLM_CONFIG
    )
    
    return response
```

## 4. 容错和验证机制

### 参数验证
```python
def validate_tool_arguments(tool_args: Dict) -> Dict:
    """验证工具函数参数的有效性"""
    validated_args = {}
    
    # 数值有效性检查
    if tool_args.get('min_price') and tool_args.get('max_price'):
        if tool_args['min_price'] > tool_args['max_price']:
            # 交换价格范围
            tool_args['min_price'], tool_args['max_price'] = tool_args['max_price'], tool_args['min_price']
    
    # 价格范围限制
    if tool_args.get('min_price') and tool_args['min_price'] < 0:
        tool_args['min_price'] = 0
    if tool_args.get('max_price') and tool_args['max_price'] > 1000:
        tool_args['max_price'] = 1000
    
    # 枚举值验证
    valid_categories = ['饭', '面', '饺子', '其他']
    if tool_args.get('category') and tool_args['category'] not in valid_categories:
        # 记录警告但不阻止查询
        print(f"警告：无效的分类值: {tool_args['category']}")
        del tool_args['category']
    
    valid_tastes = ['辣', '咸', '淡', '酸甜']
    if tool_args.get('taste') and tool_args['taste'] not in valid_tastes:
        print(f"警告：无效的口味值: {tool_args['taste']}")
        del tool_args['taste']
    
    # 辣度范围限制
    if tool_args.get('spice_level'):
        spice_level = tool_args['spice_level']
        if spice_level < 0:
            tool_args['spice_level'] = 0
        elif spice_level > 5:
            tool_args['spice_level'] = 5
    
    # 结果数量限制
    if tool_args.get('limit'):
        limit = tool_args['limit']
        if limit < 1:
            tool_args['limit'] = 1
        elif limit > 50:
            tool_args['limit'] = 50
    
    # 过滤空参数
    validated_args = {k: v for k, v in tool_args.items() if v is not None}
    
    return validated_args
```

## 5. 完整的AI推荐服务实现

### AI推荐服务类
```python
# canteen_new/ai/services.py
class AIRecommendationService:
    def __init__(self):
        self.dish_service = DishService()
    
    def process_user_query(self, user_query: str, user_preferences: Dict = None) -> Dict:
        """处理用户查询并返回推荐结果"""
        try:
            # 调用LLM
            llm_response = self.call_llm_for_recommendation(user_query, user_preferences)
            
            # 检查是否调用了工具函数
            if llm_response.choices[0].message.tool_calls:
                tool_call = llm_response.choices[0].message.tool_calls[0]
                
                if tool_call.function.name == "get_dishes_by_criteria":
                    # 解析参数
                    import json
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # 验证参数
                    validated_args = self.validate_tool_arguments(tool_args)
                    
                    # 执行查询
                    dishes = self.get_dishes_by_criteria(**validated_args)
                    
                    # 格式化响应
                    return self.format_recommendation_response(dishes, user_query)
            
            # 如果没有调用工具，返回LLM的原始响应
            return {
                "type": "chat_response",
                "content": llm_response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                "type": "error",
                "content": f"抱歉，AI推荐服务暂时不可用：{str(e)}"
            }
    
    def format_recommendation_response(self, dishes: List, user_query: str) -> Dict:
        """格式化推荐结果"""
        if not dishes:
            return {
                "type": "recommendation",
                "content": f"根据您的需求'{user_query}'，没有找到符合条件的菜品。",
                "dishes": []
            }
        
        # 构建推荐理由
        reasons = self.generate_recommendation_reasons(dishes, user_query)
        
        return {
            "type": "recommendation",
            "content": f"根据您的需求'{user_query}'，为您推荐以下{len(dishes)}个菜品：",
            "dishes": dishes,
            "reasons": reasons,
            "query_analysis": {
                "intent": "菜品查询",
                "extracted_preferences": self.extract_preferences_from_query(user_query)
            }
        }
```

## 6. 集成到现有系统

### 修改现有API
```python
# canteen_new/api/dishes.py
@api_view(['POST'])
def ai_recommend(request):
    """AI智能推荐 - 增强版本"""
    try:
        query = request.data.get('query', '')
        preferences = request.data.get('preferences', {})
        
        if not query:
            return api_validation_error("查询内容不能为空")
        
        # 调用AI推荐服务
        from canteen_new.ai.services import AIRecommendationService
        ai_service = AIRecommendationService()
        result = ai_service.process_user_query(query, preferences)
        
        return api_success(result, "AI推荐成功")
        
    except ValidationException as e:
        return api_validation_error(str(e))
    except Exception as e:
        return api_error("SERVER_001", str(e), "服务器内部错误", status.HTTP_500_INTERNAL_SERVER_ERROR)
```

## 7. 测试用例设计

### 测试场景
1. **明确查询**: "我想吃辣的面食，价格在20元以内"
2. **模糊查询**: "推荐一些好吃的"
3. **闲聊**: "今天天气怎么样"
4. **边界测试**: "价格0-1000元的特辣菜品"
5. **错误参数**: "分类为'火锅'的菜品"（无效分类）

### 预期行为
- 场景1: 调用工具函数，返回符合条件的菜品
- 场景2: 可能调用工具函数或直接回复推荐
- 场景3: 不调用工具函数，直接回复
- 场景4: 参数被自动修正到合理范围
- 场景5: 无效参数被过滤，查询继续执行

## 8. 部署和监控

### 性能监控
- 记录LLM调用成功率
- 监控工具函数调用准确率
- 跟踪用户满意度反馈
- 设置错误报警机制

### 持续优化
- 基于用户反馈调整Schema描述
- 优化LLM调用参数
- 扩展支持的查询条件
- 改进参数验证逻辑

这个实现方案确保了AI模型能够可靠地调用工具函数，并生成精确的参数字典，同时具备完善的容错和验证机制。
