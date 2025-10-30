"""
简化的LLM服务
专注于LLM通信，移除参数提取等重复逻辑
"""
import json
import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from config.llm_config import llm_config
from .utils import GET_DISHES_SCHEMA, validate_tool_arguments, get_dishes_by_criteria


class LLMService:
    """简化的LLM服务 - 专注于LLM通信"""
    
    def __init__(self):
        self.client = None
        self.setup_client()
    
    def setup_client(self):
        """设置LLM客户端"""
        config = llm_config.get_client_config()
        
        if config.get('mode') == 'mock':
            print("LLM服务: 使用模拟模式")
            self.client = None
        else:
            try:
                self.client = OpenAI(
                    api_key=config['api_key'],
                    base_url=config['base_url']
                )
                print(f"LLM服务: 已连接到 {config['provider']} - {config['model']}")
            except Exception as e:
                print(f"LLM服务: 客户端设置失败，使用模拟模式 - {e}")
                self.client = None
    
    def is_available(self) -> bool:
        """检查LLM是否可用"""
        return self.client is not None
    
    def enhance_with_context(self, user_query: str, initial_params: Dict, context_data: Dict) -> Dict[str, Any]:

        print(f"=== LLM增强处理调试 ===")
        print(f"用户查询: {user_query}")
        print(f"初始参数: {initial_params}")
        print(f"情景数据: {context_data}")
        
        try:
            # 构建系统提示
            system_prompt = self._build_enhancement_prompt(initial_params, context_data)
            
            # 构建消息
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
            
            # 调用LLM
            response = self.call_llm_with_tools(messages, [GET_DISHES_SCHEMA])
            
            # 处理LLM响应
            return self._process_llm_response(response, user_query, context_data)
            
        except Exception as e:
            print(f"LLM增强处理失败: {e}")
            return self._create_fallback_response(user_query, initial_params, context_data)
    
    def _build_enhancement_prompt(self, initial_params: Dict, context_data: Dict) -> str:
        """构建增强处理的系统提示"""
        date_info = context_data["date_info"]
        weather_info = context_data["weather_info"]
        crowd_info = context_data["crowd_info"]
        
        prompt = f"""
你是一个智能食堂菜品推荐助手。请根据以下信息为用户推荐合适的菜品：

## 当前情景数据
- **日期**：{date_info['current_date']}，{date_info['current_season']}季节，{'周末' if date_info['is_weekend'] else '工作日'}
- **节日**：{', '.join(date_info['festival_tags'])}
- **天气**：{weather_info['weather']}，温度{weather_info['temperature']}°C
- **客流**：{crowd_info['crowd_level']}，平均等待时间{crowd_info['avg_wait_time']}分钟

## 初始判断参数（必须尊重）
基于用户查询提取的初始判断参数：
{json.dumps(initial_params, ensure_ascii=False, indent=2)}

## 执行规则
1. **必须调用工具函数**：使用get_dishes_by_criteria函数查询菜品
2. **尊重初始判断**：如果情景数据与初始判断冲突，以初始判断为准
3. **合理增强**：基于情景数据合理调整参数，但不能删除初始参数
4. **简洁回应**：用简洁的语言直接回应用户输入，避免冗长
5. **生成推荐理由**：必须提供llm_reason参数，基于确定的筛选条件和情景数据合理描述推荐理由

## 推荐理由生成要求
- **简洁明了**：推荐理由要简洁，控制在1-2句话内
- **基于筛选条件**：理由必须基于实际使用的查询参数（如口味、价格、分类等）
- **结合情景**：合理结合天气、季节、客流等情景数据
- **个性化**：针对用户的具体需求提供个性化理由

## 参数调整指南
- 寒冷天气({weather_info['temperature']}°C)：可适当增加辣度或推荐热食
- 炎热天气：可推荐清淡菜品
- 高客流：可设置max_wait_time限制
- 节日：可推荐相关特色菜品

请根据用户查询，结合初始判断和情景数据，调用工具函数并生成简洁的回复和合理的推荐理由。
"""
        return prompt
    
    def call_llm_with_tools(self, messages: List[Dict], tools: List[Dict], 
                          temperature: float = 0.7, max_tokens: int = 2000):
        if self.client is None:
            return self._mock_llm_call(messages, tools)
        
        try:
            response = self.client.chat.completions.create(
                model=llm_config.model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response
        except Exception as e:
            print(f"LLM调用失败: {e}")
            return self._mock_llm_call(messages, tools)
    
    def _mock_llm_call(self, messages: List[Dict], tools: List[Dict]):
        """模拟LLM调用 - 简化版本"""
        user_message = messages[-1]['content']
        system_message = messages[0]['content'] if messages and messages[0]['role'] == 'system' else ""
        
        # 简单的模拟逻辑：直接使用初始参数
        import re
        initial_params_match = re.search(r'初始判断参数：\s*({.*?})', system_message, re.DOTALL)
        if initial_params_match:
            initial_params_str = initial_params_match.group(1)
            try:
                tool_args = json.loads(initial_params_str)
            except:
                tool_args = {}
        else:
            tool_args = {}
        
        # 添加一些基于情景数据的简单增强
        if "寒冷天气" in system_message and "taste" not in tool_args:
            tool_args["taste"] = "辣"
        if "高客流" in system_message and "max_wait_time" not in tool_args:
            tool_args["max_wait_time"] = 15
        
        return type('MockResponse', (), {
            'choices': [type('MockChoice', (), {
                'message': type('MockMessage', (), {
                    'tool_calls': [type('MockToolCall', (), {
                        'function': type('MockFunction', (), {
                            'name': "get_dishes_by_criteria",
                            'arguments': json.dumps(tool_args, ensure_ascii=False)
                        })
                    })],
                    'content': f"基于当前情景和您的需求，为您推荐以下菜品："
                })
            })]
        })()
    
    def _process_llm_response(self, response, user_query: str, context_data: Dict) -> Dict[str, Any]:
        """处理LLM响应"""
        try:
            # 检查是否调用了工具函数
            if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                
                if tool_call.function.name == "get_dishes_by_criteria":
                    # 解析参数
                    tool_args = json.loads(tool_call.function.arguments)
                    print(f"LLM生成的参数: {tool_args}")
                    
                    # 提取推荐理由
                    llm_reason = tool_args.pop('llm_reason', None) if 'llm_reason' in tool_args else None
                    if llm_reason:
                        print(f"LLM生成的推荐理由: {llm_reason}")
                    
                    # 验证参数
                    validated_args = validate_tool_arguments(tool_args)
                    
                    # 执行查询
                    dishes = get_dishes_by_criteria(**validated_args)
                    
                    # 生成响应
                    return self._generate_llm_response(dishes, user_query, context_data, response.choices[0].message.content, llm_reason)
            
            # 如果没有调用工具，返回聊天响应
            return {
                "type": "chat_response",
                "content": response.choices[0].message.content,
                "dishes": [],
                "processing_mode": "llm_chat"
            }
            
        except Exception as e:
            print(f"处理LLM响应失败: {e}")
            raise
    
    def _generate_llm_response(self, dishes: List, user_query: str, context_data: Dict, llm_content: str, llm_reason: str = None) -> Dict[str, Any]:
        """生成LLM处理的响应"""
        if not dishes:
            return {
                "type": "recommendation",
                "content": f"{llm_content}\n根据您的需求'{user_query}'，没有找到符合条件的菜品。",
                "dishes": [],
                "processing_mode": "llm_enhanced",
                "context_data": context_data
            }
        
        # 如果LLM内容为空，生成默认的推荐文本
        if not llm_content or llm_content.strip() == "":
            llm_content = self._generate_default_recommendation_text(dishes, user_query, context_data)
        
        # 生成推荐理由：优先使用LLM生成的推荐理由，如果没有则使用原有的理由生成逻辑
        if llm_reason:
            # 使用LLM生成的推荐理由
            reasons = llm_reason
            print(f"使用LLM生成的推荐理由: {llm_reason}")
        else:
            # 使用原有的理由生成逻辑
            reasons = self._generate_llm_reasons(dishes, context_data)
            print("使用原有的理由生成逻辑")
        
        return {
            "type": "recommendation",
            "content": reasons,
            "dishes": dishes,
            "reasons": self._generate_llm_reasons(dishes, context_data),
            "processing_mode": "llm_enhanced",
            "context_data": context_data
        }
    
    def _generate_default_recommendation_text(self, dishes: List, user_query: str, context_data: Dict) -> str:
        """生成默认的推荐文本"""
        if len(dishes) == 1:
            dish = dishes[0]
            return f"根据您的需求'{user_query}'，为您推荐：{dish.get('name', '未知菜品')}（{dish.get('canteen', '未知食堂')}）- ¥{dish.get('price', 0)}"
        else:
            dish_names = [dish.get('name', '未知菜品') for dish in dishes]
            return f"根据您的需求'{user_query}'，为您推荐以下{len(dishes)}个菜品：{', '.join(dish_names)}"
    
    def _generate_llm_reasons(self, dishes: List, context_data: Dict) -> List[str]:
        """生成LLM处理的推荐理由"""
        reasons = []
        weather_info = context_data["weather_info"]
        date_info = context_data["date_info"]
        
        for dish in dishes:
            reason_parts = []
            
            # 基于情景数据的理由
            temperature = weather_info['temperature']
            if temperature < 15 and dish.get('taste') == '辣':
                reason_parts.append("适合寒冷天气暖身")
            elif temperature > 25 and dish.get('taste') == '淡':
                reason_parts.append("适合炎热天气清爽")
            
            # 基于季节的理由
            season = date_info['current_season']
            if season == '冬季' and dish.get('taste') == '辣':
                reason_parts.append("冬季御寒佳品")
            elif season == '夏季' and dish.get('taste') == '淡':
                reason_parts.append("夏季清爽选择")
            
            # 基于评分的理由
            if dish.get('rating', 0) >= 4.5:
                reason_parts.append("高评分热门菜品")
            
            reasons.append("，".join(reason_parts) if reason_parts else "符合推荐条件")
        
        return reasons
    
    def _create_fallback_response(self, user_query: str, initial_params: Dict, context_data: Dict) -> Dict[str, Any]:
        """创建降级响应"""
        return {
            "type": "error",
            "content": "LLM处理失败，请稍后重试",
            "dishes": [],
            "processing_mode": "llm_fallback"
        }


# 创建全局实例
llm_service = LLMService()
