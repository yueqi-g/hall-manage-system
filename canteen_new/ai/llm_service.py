"""
LLM服务模块
集成真实LLM调用和用户收藏分析
"""
import json
import os
from typing import Dict, Any, List, Optional
from openai import OpenAI
from config.llm_config import llm_config
from .utils import GET_DISHES_SCHEMA, validate_tool_arguments, get_dishes_by_criteria
from data.services import dish_service


class LLMService:
    """LLM服务类"""
    
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
    
    def call_llm_with_tools(self, messages: List[Dict], tools: List[Dict], 
                          temperature: float = 0.7, max_tokens: int = 2000):
        """
        调用LLM并支持工具函数
        
        Args:
            messages: 消息列表
            tools: 工具函数定义
            temperature: 温度参数
            max_tokens: 最大token数
            
        Returns:
            LLM响应
        """
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
            # 降级到模拟模式
            return self._mock_llm_call(messages, tools)
    
    def _mock_llm_call(self, messages: List[Dict], tools: List[Dict]):
        """模拟LLM调用 - 增强版，结合情景数据"""
        user_message = messages[-1]['content']
        system_message = messages[0]['content'] if messages and messages[0]['role'] == 'system' else ""
        user_query = user_message.lower()
        
        # 检查是否需要调用工具函数
        should_call_tool = any(keyword in user_query for keyword in [
            '推荐', '想吃', '找', '搜索', '查询', '辣', '咸', '淡', '酸甜',
            '价格', '评分', '面', '饭', '饺子', '菜品', '菜'
        ])
        
        if should_call_tool:
            # 增强版参数提取：结合情景数据
            tool_args = self._extract_enhanced_parameters(user_message, system_message)
            
            return type('MockResponse', (), {
                'choices': [type('MockChoice', (), {
                    'message': type('MockMessage', (), {
                        'tool_calls': [type('MockToolCall', (), {
                            'function': type('MockFunction', (), {
                                'name': "get_dishes_by_criteria",
                                'arguments': json.dumps(tool_args, ensure_ascii=False)
                            })
                        })]
                    })
                })]
            })()
        else:
            # 模拟直接回复
            return type('MockResponse', (), {
                'choices': [type('MockChoice', (), {
                    'message': type('MockMessage', (), {
                        'content': "我是食堂菜品推荐助手，请问您想吃什么类型的菜品？我可以帮您推荐。"
                    })
                })]
            })()
    
    def _extract_enhanced_parameters(self, user_query: str, system_message: str) -> Dict[str, Any]:
        """增强版参数提取：结合情景数据"""
        # 基础参数提取
        params = self._extract_parameters_from_query(user_query)
        
        # 从系统提示中提取情景数据
        context_data = self._extract_context_from_system_prompt(system_message)
        
        # 基于情景数据增强参数
        if context_data:
            params = self._enhance_parameters_with_context(params, context_data)
        
        return params
    
    def _extract_context_from_system_prompt(self, system_message: str) -> Dict[str, Any]:
        """从系统提示中提取情景数据"""
        if not system_message:
            return {}
        
        context_data = {}
        
        # 提取温度信息
        import re
        temp_match = re.search(r'温度(\d+)°C', system_message)
        if temp_match:
            context_data['temperature'] = int(temp_match.group(1))
        
        # 提取季节信息
        season_match = re.search(r'(\w+)季节', system_message)
        if season_match:
            context_data['season'] = season_match.group(1)
        
        # 提取天气信息
        weather_match = re.search(r'天气：([^，]+)', system_message)
        if weather_match:
            context_data['weather'] = weather_match.group(1)
        
        # 提取客流信息
        crowd_match = re.search(r'客流：([^，]+)', system_message)
        if crowd_match:
            context_data['crowd_level'] = crowd_match.group(1)
        
        # 提取时间信息
        if '周末' in system_message:
            context_data['is_weekend'] = True
        elif '工作日' in system_message:
            context_data['is_weekend'] = False
        
        return context_data
    
    def _enhance_parameters_with_context(self, params: Dict, context_data: Dict) -> Dict[str, Any]:
        """基于情景数据增强参数"""
        # 基于温度调整口味和辣度
        temperature = context_data.get('temperature', 0)
        if temperature < 15:
            # 寒冷天气：推荐辣味暖身
            if 'taste' not in params:
                params['taste'] = '辣'
            if 'spice_level' not in params:
                params['spice_level'] = 3
            # 推荐热食类
            if 'category' not in params:
                params['category'] = '饭'
        elif temperature > 25:
            # 炎热天气：推荐清淡清爽
            if 'taste' not in params:
                params['taste'] = '淡'
            # 推荐凉菜类
            if 'category' not in params:
                params['category'] = '其他'
        
        # 基于季节调整
        season = context_data.get('season', '')
        if season == '冬季':
            if 'taste' not in params:
                params['taste'] = '辣'
        elif season == '夏季':
            if 'taste' not in params:
                params['taste'] = '淡'
        
        # 基于客流调整等待时间
        crowd_level = context_data.get('crowd_level', '')
        if crowd_level == '高':
            params['max_wait_time'] = 15
        
        # 基于时间调整
        if context_data.get('is_weekend'):
            # 周末推荐特色菜
            if 'sort_by' not in params:
                params['sort_by'] = 'rating'
        else:
            # 工作日推荐快速出餐
            if 'max_wait_time' not in params:
                params['max_wait_time'] = 15
        
        return params
    
    def _extract_parameters_from_query(self, user_query: str) -> Dict[str, Any]:
        """从用户查询中提取参数"""
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
    
    def get_user_preferences_summary(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        获取用户偏好汇总
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户偏好汇总
        """
        if user_id is None:
            # 返回通用偏好
            return {
                "preferred_categories": ["饭", "面"],
                "preferred_tastes": ["咸", "辣"],
                "budget_range": [15, 30],
                "spice_tolerance": "中等"
            }
        
        try:
            # 获取用户收藏分析
            favorites_summary = dish_service.get_user_favorites_summary(user_id)
            return favorites_summary
        except Exception as e:
            print(f"获取用户偏好失败: {e}")
            # 返回默认偏好
            return {
                "preferred_categories": ["饭", "面"],
                "preferred_tastes": ["咸", "辣"],
                "budget_range": [15, 30],
                "spice_tolerance": "中等"
            }


# 创建全局实例
llm_service = LLMService()
