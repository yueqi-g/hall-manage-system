"""
AI流程编排器
统一入口，负责协调关键词提取、情景数据、LLM处理等模块
"""
import json
from typing import Dict, Any, List, Optional
from .keyword_extractor import KeywordExtractor
from .context_service import ContextService
from .llm_service import LLMService
from .utils import get_dishes_by_criteria, validate_tool_arguments


class AIOrchestrator:
    """AI流程编排器 - 统一入口"""
    
    def __init__(self):
        self.keyword_extractor = KeywordExtractor()
        self.context_service = ContextService()
        self.llm_service = LLMService()
    
    def process_query(self, user_query: str, user_id: Optional[int] = None) -> Dict[str, Any]:
        """
        处理用户查询的主流程
        
        Args:
            user_query: 用户输入文本
            user_id: 用户ID（可选）
            
        Returns:
            推荐结果
        """
        print(f"\n=== AI流程编排器调试信息 ===")
        print(f"用户查询: {user_query}")
        print(f"用户ID: {user_id}")
        
        try:
            # 1. 第一阶段：关键词提取（初始判断）
            print("1. 关键词提取阶段...")
            initial_params = self.keyword_extractor.extract(user_query)
            print(f"初始判断参数: {initial_params}")
            
            # 2. 获取情景数据
            print("2. 获取情景数据...")
            context_data = self.context_service.get_all_context_data(user_id)
            print(f"情景数据: {context_data}")
            
            # 3. 第二阶段：决策使用LLM还是降级处理
            print("3. 决策阶段...")
            if self.llm_service.is_available():
                print("✅ LLM可用，使用增强处理")
                result = self._process_with_llm(user_query, initial_params, context_data)
            else:
                print("⚠️ LLM不可用，使用降级处理")
                result = self._process_with_keywords(user_query, initial_params, context_data)
            
            print(f"4. 最终结果: {result.get('type')}, 菜品数量: {len(result.get('dishes', []))}")
            return result
            
        except Exception as e:
            print(f"!!! 编排器异常: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._create_error_response(f"AI服务暂时不可用：{str(e)}")
    
    def _process_with_llm(self, user_query: str, initial_params: Dict, context_data: Dict) -> Dict[str, Any]:
        """
        使用LLM进行增强处理
        
        Args:
            user_query: 用户原始输入
            initial_params: 初始判断参数
            context_data: 情景数据
            
        Returns:
            增强后的推荐结果
        """
        print("=== LLM增强处理 ===")
        
        # 调用LLM服务进行增强处理
        llm_result = self.llm_service.enhance_with_context(
            user_query=user_query,
            initial_params=initial_params,
            context_data=context_data
        )
        
        # 处理LLM响应
        if llm_result.get("type") == "recommendation" or llm_result.get("type") == "chat_response":
            # LLM成功生成了推荐
            return {
                **llm_result,
                "processing_mode": "llm_enhanced",
                "context_data": context_data
            }
            
        else:
            # LLM处理失败，降级到关键词处理
            print("LLM处理失败，降级到关键词处理")
            return self._process_with_keywords(user_query, initial_params, context_data)
    
    def _process_with_keywords(self, user_query: str, initial_params: Dict, context_data: Dict) -> Dict[str, Any]:
        """
        降级处理：直接使用关键词提取结果
        
        Args:
            user_query: 用户原始输入
            initial_params: 初始判断参数
            context_data: 情景数据
            
        Returns:
            降级处理结果
        """
        print("=== 关键词降级处理 ===")
        
        # 基于情景数据增强初始参数
        enhanced_params = self._enhance_params_with_context(initial_params, context_data)
        print(f"增强后的参数: {enhanced_params}")
        
        # 执行数据库查询
        dishes = get_dishes_by_criteria(**enhanced_params)
        print(f"查询结果: {len(dishes)} 个菜品")
        
        # 生成响应
        return self._generate_keyword_response(dishes, user_query, context_data, enhanced_params)
    
    def _enhance_params_with_context(self, params: Dict, context_data: Dict) -> Dict[str, Any]:
        """
        基于情景数据增强参数
        
        Args:
            params: 原始参数
            context_data: 情景数据
            
        Returns:
            增强后的参数
        """
        enhanced_params = params.copy()
        weather_info = context_data["weather_info"]
        crowd_info = context_data["crowd_info"]
        
        # 基于天气调整
        temperature = weather_info['temperature']
        if temperature < 15 and 'taste' not in enhanced_params:
            enhanced_params['taste'] = '辣'  # 寒冷天气推荐辣味
        elif temperature > 25 and 'taste' not in enhanced_params:
            enhanced_params['taste'] = '淡'  # 炎热天气推荐清淡
        
        # 基于客流调整等待时间
        if crowd_info['crowd_level'] == '高' and 'max_wait_time' not in enhanced_params:
            enhanced_params['max_wait_time'] = 15
        
        return enhanced_params
    
    def _generate_keyword_response(self, dishes: List, user_query: str, context_data: Dict, params: Dict) -> Dict[str, Any]:
        """
        生成关键词处理的响应
        
        Args:
            dishes: 菜品列表
            user_query: 用户查询
            context_data: 情景数据
            params: 使用的参数
            
        Returns:
            格式化响应
        """
        if not dishes:
            return {
                "type": "recommendation",
                "content": f"根据您的需求'{user_query}'，没有找到符合条件的菜品。请尝试调整搜索条件。",
                "dishes": [],
                "processing_mode": "keyword_fallback",
                "context_data": context_data,
                "query_analysis": {
                    "intent": "菜品查询",
                    "extracted_params": params
                }
            }
        
        # 生成简洁的推荐文本
        content = self._generate_clean_recommendation_text(dishes, user_query, context_data)
        
        return {
            "type": "recommendation",
            "content": content,
            "dishes": dishes,  # 保留菜品数据供前端使用
            "processing_mode": "keyword_fallback",
            "context_data": context_data,
            "query_analysis": {
                "intent": "菜品查询",
                "extracted_params": params
            }
        }
    
    def _generate_fallback_reasons(self, dishes: List, user_query: str, context_data: Dict) -> List[str]:
        """
        生成降级处理的推荐理由
        
        Args:
            dishes: 菜品列表
            user_query: 用户查询
            context_data: 情景数据
            
        Returns:
            推荐理由列表
        """
        reasons = []
        query_lower = user_query.lower()
        weather_info = context_data["weather_info"]
        
        for dish in dishes:
            reason_parts = []
            
            # 基于天气的推荐理由
            temperature = weather_info['temperature']
            if temperature < 15 and dish.get('taste') == '辣':
                reason_parts.append(f"适合{temperature}°C寒冷天气暖身")
            elif temperature > 25 and dish.get('taste') == '淡':
                reason_parts.append(f"适合{temperature}°C炎热天气清爽")
            
            # 基于用户查询的推荐理由
            if '辣' in query_lower and dish.get('taste') == '辣':
                reason_parts.append("符合您的辣味需求")
            if '实惠' in query_lower and dish.get('price', 0) < 20:
                reason_parts.append("价格实惠")
            
            # 基于评分的推荐理由
            if dish.get('rating', 0) >= 4.5:
                reason_parts.append("高评分热门菜品")
            
            # 默认理由
            if not reason_parts:
                reason_parts.append("符合您的搜索条件")
            
            reasons.append("，".join(reason_parts))
        
        return reasons
    
    def _generate_clean_recommendation_text(self, dishes: List, user_query: str, context_data: Dict) -> str:
        """
        生成简洁美观的推荐文本（使用HTML换行）
        
        Args:
            dishes: 菜品列表
            user_query: 用户查询
            context_data: 情景数据
            
        Returns:
            简洁的推荐文本（HTML格式）
        """
        if len(dishes) == 1:
            dish = dishes[0]
            # 单菜品推荐：简洁格式
            dish_name = dish.get('name', '未知菜品')
            canteen = dish.get('canteen', '未知食堂')
            price = dish.get('price', 0)
            
            # 生成简洁的推荐理由
            reasons = self._generate_clean_reasons(dish, user_query, context_data)
            
            return f"为您推荐：{dish_name}（{canteen}）- ¥{price}<br>推荐理由：{reasons}"
        else:
            # 多菜品推荐：列表格式
            text_lines = [f"为您推荐以下{len(dishes)}个菜品："]
            
            for i, dish in enumerate(dishes, 1):
                dish_name = dish.get('name', '未知菜品')
                canteen = dish.get('canteen', '未知食堂')
                price = dish.get('price', 0)
                
                # 生成简洁的推荐理由
                reasons = self._generate_clean_reasons(dish, user_query, context_data)
                
                text_lines.append(f"{i}. {dish_name}（{canteen}）- ¥{price}")
                text_lines.append(f"   推荐理由：{reasons}")
            
            return "<br>".join(text_lines)
    
    def _generate_clean_reasons(self, dish: Dict, user_query: str, context_data: Dict) -> str:
        """
        生成简洁的推荐理由
        
        Args:
            dish: 菜品信息
            user_query: 用户查询
            context_data: 情景数据
            
        Returns:
            简洁的推荐理由
        """
        reasons = []
        query_lower = user_query.lower()
        weather_info = context_data["weather_info"]
        
        # 基于用户查询的推荐理由
        if '辣' in query_lower and dish.get('taste') == '辣':
            reasons.append("辣味菜品")
        if '实惠' in query_lower and dish.get('price', 0) < 20:
            reasons.append("价格实惠")
        if '面' in query_lower and dish.get('category') == '面':
            reasons.append("面食类")
        if '饭' in query_lower and dish.get('category') == '饭':
            reasons.append("主食类")
        
        # 基于天气的推荐理由
        temperature = weather_info['temperature']
        if temperature < 15 and dish.get('taste') == '辣':
            reasons.append("适合寒冷天气")
        elif temperature > 25 and dish.get('taste') == '淡':
            reasons.append("适合炎热天气")
        
        # 基于评分的推荐理由
        rating = dish.get('rating', 0)
        if rating >= 4.5:
            reasons.append("高评分")
        elif rating >= 4.0:
            reasons.append("评分不错")
        
        # 如果还没有理由，使用默认理由
        if not reasons:
            reasons.append("符合您的需求")
        
        # 限制理由数量，选择最相关的2-3个
        if len(reasons) > 3:
            reasons = reasons[:3]
        
        return "，".join(reasons)
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """创建错误响应"""
        return {
            "type": "error",
            "content": error_message,
            "dishes": [],
            "processing_mode": "error"
        }


# 创建全局实例
ai_orchestrator = AIOrchestrator()
