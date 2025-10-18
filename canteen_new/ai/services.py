"""
AI推荐服务层
实现LLM调用和智能推荐功能
"""
import json
from typing import Dict, Any, List, Optional
from .utils import GET_DISHES_SCHEMA, get_dishes_by_criteria, validate_tool_arguments
from .context_service import ContextService


class AIRecommendationService:
    """AI推荐服务类"""
    
    def __init__(self):
        from data.services import dish_service
        self.dish_service = dish_service
        self.context_service = ContextService()
    
    def call_llm_for_recommendation(self, user_query: str, user_preferences: Dict = None):
        """
        调用LLM进行智能推荐（使用真实LLM服务）
        
        Args:
            user_query: 用户查询
            user_preferences: 用户偏好
            
        Returns:
            LLM响应
        """
        print(f"\n=== 调用真实LLM服务 - 详细调试 ===")
        print(f"用户查询: {user_query}")
        print(f"用户偏好: {user_preferences}")
        
        # 构建系统提示
        system_prompt = """你是一个食堂菜品推荐助手。根据用户需求，调用合适的工具函数查询菜品。
        如果用户需求明确涉及菜品查询，调用get_dishes_by_criteria函数。
        如果只是闲聊或非菜品相关查询，直接回复而不调用工具。"""
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        print(f"消息内容: {messages}")
        
        # 调用真实LLM服务
        from .llm_service import llm_service
        print(f"1. LLM服务状态: {llm_service.client}")
        print(f"2. LLM配置: {llm_service.setup_client()}")
        
        try:
            print("3. 开始调用LLM API...")
            response = llm_service.call_llm_with_tools(
                messages=messages,
                tools=[GET_DISHES_SCHEMA]
            )
            
            print(f"4. LLM响应类型: {type(response)}")
            print(f"5. LLM响应对象: {response}")
            
            # 检查是否是模拟响应
            if hasattr(response, '__class__') and 'MockResponse' in str(response.__class__):
                print("⚠️ 使用模拟LLM响应")
            else:
                print("✅ 使用真实LLM响应")
                
            # 详细分析响应内容
            if hasattr(response, 'choices') and response.choices:
                choice = response.choices[0]
                print(f"6. 第一个选择: {choice}")
                if hasattr(choice, 'message'):
                    message = choice.message
                    print(f"7. 消息内容: {message}")
                    if hasattr(message, 'content') and message.content:
                        print(f"8. 直接回复内容: {message.content}")
                    if hasattr(message, 'tool_calls') and message.tool_calls:
                        print(f"9. 工具调用数量: {len(message.tool_calls)}")
                        for i, tool_call in enumerate(message.tool_calls):
                            print(f"   工具调用 {i+1}: {tool_call}")
                            if hasattr(tool_call, 'function'):
                                print(f"   函数名称: {tool_call.function.name}")
                                print(f"   函数参数: {tool_call.function.arguments}")
                
            return response
            
        except Exception as e:
            print(f"❌ LLM调用失败: {e}")
            import traceback
            traceback.print_exc()
            # 降级到模拟模式
            print("🔄 降级到模拟LLM模式")
            return self._mock_llm_call(user_query)
    
    def _mock_llm_call(self, user_query: str):
        """模拟LLM调用（降级模式）"""
        print("⚠️ 降级到模拟LLM模式")
        query_lower = user_query.lower()
        
        # 检查是否需要调用工具函数
        should_call_tool = any(keyword in query_lower for keyword in [
            '推荐', '想吃', '找', '搜索', '查询', '辣', '咸', '淡', '酸甜',
            '价格', '评分', '面', '饭', '饺子', '菜品', '菜'
        ])
        
        if should_call_tool:
            # 模拟工具函数调用
            tool_args = self.extract_parameters_from_query(user_query)
            
            return {
                "choices": [{
                    "message": {
                        "tool_calls": [{
                            "function": {
                                "name": "get_dishes_by_criteria",
                                "arguments": json.dumps(tool_args, ensure_ascii=False)
                            }
                        }]
                    }
                }]
            }
        else:
            # 模拟直接回复
            return {
                "choices": [{
                    "message": {
                        "content": "我是食堂菜品推荐助手，请问您想吃什么类型的菜品？我可以帮您推荐。"
                    }
                }]
            }
    
    def extract_parameters_from_query(self, user_query: str) -> Dict[str, Any]:
        """
        从用户查询中提取参数（模拟实现）
        
        Args:
            user_query: 用户查询
            
        Returns:
            提取的参数
        """
        query_lower = user_query.lower()
        params = {}
        
        # 提取分类
        if '面' in query_lower:
            params['category'] = '面'
        elif '饭' in query_lower:
            params['category'] = '饭'
        elif '饺子' in query_lower:
            params['category'] = '饺子'
        
        # 提取口味
        if '辣' in query_lower:
            params['taste'] = '辣'
            if '特辣' in query_lower or '很辣' in query_lower:
                params['spice_level'] = 5
            elif '中辣' in query_lower:
                params['spice_level'] = 3
            elif '微辣' in query_lower:
                params['spice_level'] = 1
            else:
                params['spice_level'] = 2
        elif '咸' in query_lower:
            params['taste'] = '咸'
        elif '淡' in query_lower:
            params['taste'] = '淡'
        elif '酸甜' in query_lower:
            params['taste'] = '酸甜'
        
        # 提取价格范围
        if '便宜' in query_lower or '实惠' in query_lower:
            params['min_price'] = 0
            params['max_price'] = 20
        elif '中等' in query_lower:
            params['min_price'] = 15
            params['max_price'] = 35
        elif '贵' in query_lower or '高档' in query_lower:
            params['min_price'] = 30
            params['max_price'] = 100
        
        # 提取具体价格
        import re
        price_pattern = r'(\d+)[元块]'
        prices = re.findall(price_pattern, user_query)
        if len(prices) == 1:
            price = int(prices[0])
            params['max_price'] = price
        elif len(prices) >= 2:
            params['min_price'] = min(int(prices[0]), int(prices[1]))
            params['max_price'] = max(int(prices[0]), int(prices[1]))
        
        # 设置默认限制
        params['limit'] = 5
        
        return params
    
    def process_user_query(self, user_query: str, user_preferences: Dict = None) -> Dict:
        """
        处理用户查询并返回推荐结果
        
        Args:
            user_query: 用户查询
            user_preferences: 用户偏好
            
        Returns:
            推荐结果
        """
        print(f"\n=== AI推荐服务调试信息 ===")
        print(f"用户查询: {user_query}")
        print(f"用户偏好: {user_preferences}")
        
        try:
            # 调用LLM
            print("1. 开始调用LLM...")
            llm_response = self.call_llm_for_recommendation(user_query, user_preferences)
            print(f"LLM响应类型: {type(llm_response)}")
            
            # 检查是否调用了工具函数
            if hasattr(llm_response.choices[0].message, 'tool_calls') and llm_response.choices[0].message.tool_calls:
                print("2. 检测到工具函数调用")
                tool_call = llm_response.choices[0].message.tool_calls[0]
                print(f"工具函数名称: {tool_call.function.name}")
                
                if tool_call.function.name == "get_dishes_by_criteria":
                    # 解析参数
                    print("3. 解析工具函数参数...")
                    tool_args = json.loads(tool_call.function.arguments)
                    print(f"原始参数: {tool_args}")
                    
                    # 验证参数
                    print("4. 验证参数...")
                    validated_args = validate_tool_arguments(tool_args)
                    print(f"验证后参数: {validated_args}")
                    
                    # 执行查询
                    print("5. 执行菜品查询...")
                    dishes = get_dishes_by_criteria(**validated_args)
                    print(f"查询结果: 找到 {len(dishes)} 个菜品")
                    
                    # 格式化响应
                    print("6. 格式化响应...")
                    return self.format_recommendation_response(dishes, user_query)
            
            # 如果没有调用工具，返回LLM的原始响应
            print("7. 未调用工具函数，返回聊天响应")
            return {
                "type": "chat_response",
                "content": llm_response.choices[0].message.content,
                "dishes": []
            }
            
        except Exception as e:
            print(f"!!! 发生异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "type": "error",
                "content": f"抱歉，AI推荐服务暂时不可用：{str(e)}",
                "dishes": []
            }
    
    def format_recommendation_response(self, dishes: List, user_query: str) -> Dict:
        """
        格式化推荐结果
        
        Args:
            dishes: 菜品列表
            user_query: 用户查询
            
        Returns:
            格式化后的推荐结果
        """
        print(f"8. 格式化推荐结果: 有 {len(dishes)} 个菜品")
        for i, dish in enumerate(dishes[:3]):
            print(f"   菜品 {i+1}: {dish.get('name')} - ¥{dish.get('price')} - {dish.get('taste')}")
        
        if not dishes:
            print("9. 没有菜品，返回空结果")
            return {
                "type": "recommendation",
                "content": f"根据您的需求'{user_query}'，没有找到符合条件的菜品。请尝试调整搜索条件。",
                "dishes": [],
                "query_analysis": {
                    "intent": "菜品查询",
                    "extracted_preferences": self.extract_preferences_from_query(user_query)
                }
            }
        
        # 构建推荐理由
        reasons = self.generate_recommendation_reasons(dishes, user_query)
        print(f"9. 生成推荐理由: {len(reasons)} 个理由")
        
        response = {
            "type": "recommendation",
            "content": f"根据您的需求'{user_query}'，为您推荐以下{len(dishes)}个菜品：",
            "dishes": dishes,
            "reasons": reasons,
            "query_analysis": {
                "intent": "菜品查询",
                "extracted_preferences": self.extract_preferences_from_query(user_query)
            }
        }
        
        print(f"10. 最终响应: {response}")
        return response
    
    def generate_recommendation_reasons(self, dishes: List, user_query: str) -> List[str]:
        """
        生成推荐理由
        
        Args:
            dishes: 菜品列表
            user_query: 用户查询
            
        Returns:
            推荐理由列表
        """
        reasons = []
        query_lower = user_query.lower()
        
        for dish in dishes:
            reason_parts = []
            
            # 基于口味匹配
            if '辣' in query_lower and dish.get('taste') == '辣':
                reason_parts.append("符合您的辣味需求")
            
            # 基于价格匹配
            if '便宜' in query_lower and dish.get('price', 0) < 20:
                reason_parts.append("价格实惠")
            elif '中等' in query_lower and 15 <= dish.get('price', 0) <= 35:
                reason_parts.append("价格适中")
            
            # 基于评分
            if dish.get('rating', 0) >= 4.5:
                reason_parts.append("评分很高")
            elif dish.get('rating', 0) >= 4.0:
                reason_parts.append("评分不错")
            
            # 默认理由
            if not reason_parts:
                reason_parts.append("符合您的搜索条件")
            
            reasons.append("，".join(reason_parts))
        
        return reasons
    
    def extract_preferences_from_query(self, user_query: str) -> Dict[str, Any]:
        """
        从用户查询中提取偏好信息
        
        Args:
            user_query: 用户查询
            
        Returns:
            提取的偏好信息
        """
        preferences = {}
        query_lower = user_query.lower()
        
        # 提取口味偏好
        if '辣' in query_lower:
            preferences['taste'] = '辣'
        elif '咸' in query_lower:
            preferences['taste'] = '咸'
        elif '淡' in query_lower:
            preferences['taste'] = '淡'
        elif '酸甜' in query_lower:
            preferences['taste'] = '酸甜'
        
        # 提取价格偏好
        if '便宜' in query_lower or '实惠' in query_lower:
            preferences['budget'] = 'low'
        elif '中等' in query_lower:
            preferences['budget'] = 'medium'
        elif '贵' in query_lower or '高档' in query_lower:
            preferences['budget'] = 'high'
        
        # 提取分类偏好
        if '面' in query_lower:
            preferences['category'] = '面'
        elif '饭' in query_lower:
            preferences['category'] = '饭'
        elif '饺子' in query_lower:
            preferences['category'] = '饺子'
        
        return preferences
    
    def process_user_query_with_context(self, user_query: str, user_id: Optional[int] = None) -> Dict:
        """
        基于情景数据的智能推荐处理
        
        Args:
            user_query: 用户查询
            user_id: 用户ID
            
        Returns:
            推荐结果
        """
        print(f"\n=== 基于情景数据的AI推荐服务调试信息 ===")
        print(f"用户查询: {user_query}")
        print(f"用户ID: {user_id}")
        
        try:
            # 1. 收集情景数据
            print("1. 收集情景数据...")
            context_data = self.context_service.get_all_context_data(user_id)
            print(f"情景数据: {context_data}")
            
            # 2. 构建增强的系统提示
            print("2. 构建增强的系统提示...")
            system_prompt = self._build_context_aware_system_prompt(context_data)
            
            # 3. 调用LLM（模拟实现）
            print("3. 调用LLM...")
            llm_response = self._call_context_aware_llm(user_query, system_prompt)
            
            # 4. 处理工具函数调用
            if hasattr(llm_response.choices[0].message, 'tool_calls') and llm_response.choices[0].message.tool_calls:
                print("4. 检测到工具函数调用")
                tool_call = llm_response.choices[0].message.tool_calls[0]
                
                if tool_call.function.name == "get_dishes_by_criteria":
                    # 解析参数
                    print("5. 解析工具函数参数...")
                    tool_args = json.loads(tool_call.function.arguments)
                    print(f"原始参数: {tool_args}")
                    
                    # 验证参数
                    print("6. 验证参数...")
                    validated_args = validate_tool_arguments(tool_args)
                    print(f"验证后参数: {validated_args}")
                    
                    # 执行查询
                    print("7. 执行菜品查询...")
                    dishes = get_dishes_by_criteria(**validated_args)
                    print(f"查询结果: 找到 {len(dishes)} 个菜品")
                    
                    # 格式化响应
                    print("8. 格式化响应...")
                    return self._format_context_aware_response(dishes, user_query, context_data)
            
            # 如果没有调用工具，返回LLM的原始响应
            print("9. 未调用工具函数，返回聊天响应")
            return {
                "type": "chat_response",
                "content": llm_response.choices[0].message.content,
                "dishes": [],
                "context_data": context_data
            }
            
        except Exception as e:
            print(f"!!! 发生异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "type": "error",
                "content": f"抱歉，AI推荐服务暂时不可用：{str(e)}",
                "dishes": []
            }
    
    def _build_context_aware_system_prompt(self, context_data: Dict) -> str:
        """构建包含情景数据的系统提示"""
        date_info = context_data["date_info"]
        weather_info = context_data["weather_info"]
        crowd_info = context_data["crowd_info"]
        user_prefs = context_data["user_preferences"]
        
        # 基于情景数据的强制推理逻辑
        temperature = weather_info['temperature']
        season = date_info['current_season']
        is_weekend = date_info['is_weekend']
        crowd_level = crowd_info['crowd_level']
        
        # 根据情景数据生成具体的推理指令
        context_reasoning = []
        
        # 天气推理
        if temperature < 15:
            context_reasoning.append(f"当前温度{temperature}°C较低，属于寒冷天气，必须优先推荐辣味、热汤、高热量菜品来暖身")
        elif temperature > 25:
            context_reasoning.append(f"当前温度{temperature}°C较高，属于炎热天气，必须优先推荐清淡、凉菜、汤品来解暑")
        else:
            context_reasoning.append(f"当前温度{temperature}°C适中，可根据用户需求灵活推荐")
        
        # 季节推理
        if season == '春季':
            context_reasoning.append(f"当前是{season}，适合推荐清淡养肝菜品")
        elif season == '夏季':
            context_reasoning.append(f"当前是{season}，适合推荐清热解暑菜品")
        elif season == '秋季':
            context_reasoning.append(f"当前是{season}，适合推荐润燥养肺菜品")
        elif season == '冬季':
            context_reasoning.append(f"当前是{season}，适合推荐温补御寒菜品")
        
        # 时间推理
        if is_weekend:
            context_reasoning.append(f"今天是周末，适合推荐特色菜、聚会菜")
        else:
            context_reasoning.append(f"今天是工作日，适合推荐快速出餐菜品")
        
        # 客流推理
        if crowd_level == '高':
            context_reasoning.append(f"当前客流{crowd_level}，必须设置max_wait_time=15限制等待时间")
        else:
            context_reasoning.append(f"当前客流{crowd_level}，可以推荐制作时间较长的特色菜")
        
        context_reasoning_text = "\n".join([f"- {reason}" for reason in context_reasoning])
        
        # 基于情景数据生成强制参数
        forced_params = {}
        
        # 强制天气参数
        if temperature < 15:
            forced_params["taste"] = "辣"
            forced_params["spice_level"] = 3
        elif temperature > 25:
            forced_params["taste"] = "淡"
        
        # 强制客流参数
        if crowd_level == '高':
            forced_params["max_wait_time"] = 15
        
        # 强制季节参数
        if season == '冬季':
            forced_params["category"] = "饭"  # 推荐主食类
        elif season == '夏季':
            forced_params["category"] = "其他"  # 推荐沙拉等
        
        forced_params_text = json.dumps(forced_params, ensure_ascii=False)
        
        prompt = f"""
你是一个智能食堂菜品推荐助手。请严格按照以下情景推理结果进行菜品推荐：

## 当前情景数据
- **日期**：{date_info['current_date']}，{season}季节，{'周末' if is_weekend else '工作日'}
- **节日**：{', '.join(date_info['festival_tags'])}
- **天气**：{weather_info['weather']}，温度{temperature}°C，湿度{weather_info['humidity']}%
- **客流**：{crowd_level}，平均等待时间{crowd_info['avg_wait_time']}分钟
- **用户偏好**：偏好{user_prefs.get('preferred_categories', [])}类别，{user_prefs.get('preferred_tastes', [])}口味

## 强制情景推理结果（必须遵守）
{context_reasoning_text}

## 强制参数要求（必须包含在工具调用中）
基于上述情景推理，你必须在工具函数参数中包含以下强制参数：
{forced_params_text}

## 工具函数调用要求
你必须调用get_dishes_by_criteria函数，并在参数中体现以下情景推理结果：

1. **必须包含的参数**：
   - category: 根据季节和用户偏好确定
   - taste: 根据天气和用户偏好确定  
   - spice_level: 根据温度确定（寒冷天气推荐高辣度）
   - max_wait_time: 根据客流情况确定
   - sort_by: 根据情景需求确定（如价格、评分等）

2. **参数示例**：
   - 寒冷天气：{{"taste": "辣", "spice_level": 3, "category": "饭"}}
   - 炎热天气：{{"taste": "淡", "category": "其他"}}
   - 高客流：{{"max_wait_time": 15}}
   - 周末：{{"sort_by": "rating"}}

## 执行规则
1. 必须基于情景推理结果生成参数，不能仅依赖用户查询
2. 如果用户需求与情景推理冲突，以情景推理为准
3. 必须在参数中体现至少2个情景因素
4. 必须调用工具函数，不能直接回复
5. 必须包含上述强制参数

现在请根据用户查询，结合上述强制情景推理结果调用工具函数。
"""
        return prompt
    
    def _call_context_aware_llm(self, user_query: str, system_prompt: str):
        """调用基于情景数据的LLM（使用真实LLM服务）"""
        print(f"=== 调用基于情景数据的真实LLM服务 ===")
        print(f"用户查询: {user_query}")
        print(f"系统提示长度: {len(system_prompt)}")
        
        # 构建消息
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        # 调用真实LLM服务
        from .llm_service import llm_service
        print(f"LLM服务状态: {llm_service.client}")
        
        try:
            response = llm_service.call_llm_with_tools(
                messages=messages,
                tools=[GET_DISHES_SCHEMA]
            )
            
            print(f"LLM响应类型: {type(response)}")
            
            # 检查是否是模拟响应
            if hasattr(response, '__class__') and 'MockResponse' in str(response.__class__):
                print("⚠️ 使用模拟LLM响应")
            else:
                print("✅ 使用真实LLM响应")
                
            return response
            
        except Exception as e:
            print(f"LLM调用失败: {e}")
            # 降级到模拟模式
            return self._mock_context_aware_llm(user_query, system_prompt)
    
    def _mock_context_aware_llm(self, user_query: str, system_prompt: str):
        """模拟基于情景数据的LLM调用（降级模式）"""
        print("⚠️ 降级到模拟LLM模式")
        query_lower = user_query.lower()
        
        # 检查是否需要调用工具函数
        should_call_tool = any(keyword in query_lower for keyword in [
            '推荐', '想吃', '找', '搜索', '查询', '辣', '咸', '淡', '酸甜',
            '价格', '评分', '面', '饭', '饺子', '菜品', '菜'
        ])
        
        if should_call_tool:
            # 模拟基于情景数据的参数提取
            tool_args = self._extract_context_aware_parameters(user_query)
            
            return {
                "choices": [{
                    "message": {
                        "tool_calls": [{
                            "function": {
                                "name": "get_dishes_by_criteria",
                                "arguments": json.dumps(tool_args, ensure_ascii=False)
                            }
                        }]
                    }
                }]
            }
        else:
            # 模拟直接回复
            return {
                "choices": [{
                    "message": {
                        "content": f"基于当前情景，我是食堂菜品推荐助手。当前天气{system_prompt.split('天气：')[1].split('，')[0]}，请问您想吃什么类型的菜品？我可以帮您推荐。"
                    }
                }]
            }
    
    def _extract_context_aware_parameters(self, user_query: str) -> Dict[str, Any]:
        """基于情景数据提取参数（模拟实现）"""
        # 获取当前情景数据
        context_data = self.context_service.get_all_context_data()
        crowd_info = context_data["crowd_info"]
        weather_info = context_data["weather_info"]
        
        # 基础参数提取
        params = self.extract_parameters_from_query(user_query)
        
        # 基于情景数据调整参数
        # 高客流时自动限制等待时间
        if crowd_info['crowd_level'] == '高':
            params['max_wait_time'] = 15
        
        # 寒冷天气推荐热食
        if weather_info['temperature'] < 10:
            if 'taste' not in params:
                params['taste'] = '辣'  # 默认推荐辣味暖身
            params['category'] = '饭'  # 推荐主食类
        
        # 炎热天气推荐清淡
        elif weather_info['temperature'] > 25:
            if 'taste' not in params:
                params['taste'] = '淡'
            params['category'] = '其他'  # 推荐沙拉等
        
        return params
    
    def _format_context_aware_response(self, dishes: List, user_query: str, context_data: Dict) -> Dict:
        """格式化基于情景数据的推荐结果"""
        print(f"10. 格式化基于情景数据的推荐结果: 有 {len(dishes)} 个菜品")
        
        if not dishes:
            return {
                "type": "recommendation",
                "content": f"根据您的需求'{user_query}'和当前情景，没有找到符合条件的菜品。请尝试调整搜索条件。",
                "dishes": [],
                "context_data": context_data,
                "query_analysis": {
                    "intent": "菜品查询",
                    "extracted_preferences": self.extract_preferences_from_query(user_query)
                }
            }
        
        # 构建基于情景的推荐理由
        reasons = self._generate_context_aware_reasons(dishes, user_query, context_data)
        
        response = {
            "type": "recommendation",
            "content": f"基于当前情景和您的需求'{user_query}'，为您推荐以下{len(dishes)}个菜品：",
            "dishes": dishes,
            "reasons": reasons,
            "context_data": context_data,
            "query_analysis": {
                "intent": "菜品查询",
                "extracted_preferences": self.extract_preferences_from_query(user_query)
            }
        }
        
        print(f"11. 最终响应: {response}")
        return response
    
    def _generate_context_aware_reasons(self, dishes: List, user_query: str, context_data: Dict) -> List[str]:
        """生成基于情景数据的推荐理由"""
        reasons = []
        weather_info = context_data["weather_info"]
        crowd_info = context_data["crowd_info"]
        date_info = context_data["date_info"]
        user_prefs = context_data["user_preferences"]
        
        for dish in dishes:
            reason_parts = []
            
            # 基于天气的推荐理由
            temperature = weather_info['temperature']
            if temperature < 15:
                if dish.get('taste') == '辣':
                    reason_parts.append(f"适合{temperature}°C寒冷天气暖身")
                elif '汤' in dish.get('name', '') or '热' in dish.get('name', ''):
                    reason_parts.append("热食适合寒冷天气")
            elif temperature > 25:
                if dish.get('taste') == '淡':
                    reason_parts.append(f"适合{temperature}°C炎热天气清爽")
                elif '凉' in dish.get('name', '') or '沙拉' in dish.get('name', ''):
                    reason_parts.append("清凉菜品适合炎热天气")
            
            # 基于季节的推荐理由
            season = date_info['current_season']
            if season == '春季' and dish.get('taste') == '淡':
                reason_parts.append("春季清淡菜品养肝")
            elif season == '夏季' and dish.get('taste') == '酸甜':
                reason_parts.append("夏季酸甜开胃")
            elif season == '秋季' and dish.get('taste') == '咸':
                reason_parts.append("秋季咸味润燥")
            elif season == '冬季' and dish.get('taste') == '辣':
                reason_parts.append("冬季辣味御寒")
            
            # 基于时间的推荐理由
            if date_info['is_weekend']:
                if dish.get('price', 0) > 25:
                    reason_parts.append("周末特色菜品")
                elif '聚会' in dish.get('description', '') or '分享' in dish.get('description', ''):
                    reason_parts.append("适合周末聚餐")
            else:
                if dish.get('price', 0) < 20:
                    reason_parts.append("工作日实惠选择")
                elif '快速' in dish.get('description', '') or '便捷' in dish.get('description', ''):
                    reason_parts.append("工作日快速出餐")
            
            # 基于客流的推荐理由
            if crowd_info['crowd_level'] == '高':
                if dish.get('price', 0) < 25:
                    reason_parts.append("高峰期实惠选择")
                elif '快速' in dish.get('description', '') or '便捷' in dish.get('description', ''):
                    reason_parts.append("高峰期快速出餐")
            else:
                if dish.get('price', 0) > 30:
                    reason_parts.append("低客流时享受特色")
                elif '特色' in dish.get('description', '') or '招牌' in dish.get('description', ''):
                    reason_parts.append("适合悠闲品尝")
            
            # 基于用户偏好的推荐理由
            if dish.get('category') in user_prefs.get('preferred_categories', []):
                reason_parts.append("符合您的类别偏好")
            if dish.get('taste') in user_prefs.get('preferred_tastes', []):
                reason_parts.append("符合您的口味偏好")
            
            # 基于评分的推荐理由
            rating = dish.get('rating', 0)
            if rating >= 4.8:
                reason_parts.append("超高评分菜品")
            elif rating >= 4.5:
                reason_parts.append("高评分热门菜品")
            elif rating >= 4.0:
                reason_parts.append("评分不错")
            
            # 基于价格的推荐理由
            price = dish.get('price', 0)
            if price < 15:
                reason_parts.append("价格非常实惠")
            elif price < 25:
                reason_parts.append("价格适中")
            elif price > 35:
                reason_parts.append("特色高端菜品")
            
            # 基于用户查询的推荐理由
            query_lower = user_query.lower()
            if '辣' in query_lower and dish.get('taste') == '辣':
                reason_parts.append("符合您的辣味需求")
            if '实惠' in query_lower or '便宜' in query_lower and price < 20:
                reason_parts.append("符合您的实惠需求")
            if '面' in query_lower and dish.get('category') == '面':
                reason_parts.append("符合您的面食需求")
            
            # 如果还没有理由，使用智能默认理由
            if not reason_parts:
                # 基于菜品特点的默认理由
                if dish.get('rating', 0) >= 4.5:
                    reason_parts.append("高评分热门选择")
                elif dish.get('price', 0) < 20:
                    reason_parts.append("性价比很高")
                else:
                    reason_parts.append("符合您的搜索条件")
            
            # 限制理由数量，选择最相关的2-3个
            if len(reason_parts) > 3:
                # 优先保留情景相关的理由
                context_reasons = [r for r in reason_parts if any(keyword in r for keyword in ['天气', '季节', '周末', '客流'])]
                other_reasons = [r for r in reason_parts if r not in context_reasons]
                reason_parts = context_reasons[:2] + other_reasons[:1]
            
            reasons.append("，".join(reason_parts))
        
        return reasons


# 创建服务实例
ai_recommendation_service = AIRecommendationService()
