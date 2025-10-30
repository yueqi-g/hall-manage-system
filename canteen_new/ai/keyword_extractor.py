"""
关键词提取器
负责从用户输入中提取关键词，生成初始判断参数
"""
import re
from typing import Dict, Any, List


class KeywordExtractor:
    
    def __init__(self):
        # 定义关键词映射
        self.category_keywords = {
            '面': ['面', '面条', '拉面', '刀削面', '牛肉面'],
            '饭': ['饭', '米饭', '炒饭', '盖饭', '套餐'],
            '饺子': ['饺子', '水饺', '蒸饺', '煎饺'],
            '其他': ['汤', '粥', '小吃', '凉菜', '热菜']
        }
        
        self.taste_keywords = {
            '辣': ['辣', '麻辣', '香辣', '酸辣', '特辣', '中辣', '微辣'],
            '咸': ['咸', '咸香', '酱香'],
            '淡': ['淡', '清淡', '爽口', '原味'],
            '酸甜': ['酸甜', '糖醋', '甜', '酸']
        }
        
        self.budget_keywords = {
            'low': ['便宜', '实惠', '经济', '低价', '省钱'],
            'medium': ['中等', '适中', '正常', '一般'],
            'high': ['贵', '高档', '豪华', '奢侈', '特色']
        }
    
    def extract(self, user_query: str) -> Dict[str, Any]:
        """
        从用户查询中提取关键词，生成初始判断参数
        
        Args:
            user_query: 用户输入文本
            
        Returns:
            初始判断参数
        """
        print(f"=== 关键词提取调试 ===")
        print(f"原始查询: {user_query}")
        
        query_lower = user_query.lower()
        params = {}
        
        # 1. 提取分类
        category = self._extract_category(query_lower)
        if category:
            params['category'] = category
            print(f"提取分类: {category}")
        
        # 2. 提取口味
        taste = self._extract_taste(query_lower)
        if taste:
            params['taste'] = taste
            print(f"提取口味: {taste}")
        
        # 3. 提取辣度级别
        spice_level = self._extract_spice_level(query_lower)
        if spice_level is not None:
            params['spice_level'] = spice_level
            print(f"提取辣度: {spice_level}")
        
        # 4. 提取价格范围
        price_params = self._extract_price(query_lower)
        if price_params:
            params.update(price_params)
            print(f"提取价格: {price_params}")
        
        # 5. 提取具体菜品名称
        dish_name = self._extract_dish_name(query_lower)
        if dish_name:
            params['name'] = dish_name
            print(f"提取菜品名称: {dish_name}")
        
        # 6. 设置默认限制
        if not params.get('limit'):
            params['limit'] = 5
        
        print(f"最终参数: {params}")
        return params
    
    def _extract_category(self, query: str) -> str:
        """提取菜品分类"""
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return category
        return ""
    
    def _extract_taste(self, query: str) -> str:
        """提取口味偏好"""
        for taste, keywords in self.taste_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    return taste
        return ""
    
    def _extract_spice_level(self, query: str) -> int:
        """提取辣度级别"""
        if '特辣' in query or '很辣' in query:
            return 5
        elif '中辣' in query:
            return 3
        elif '微辣' in query:
            return 1
        elif '辣' in query:
            return 5  # 默认辣度
        return None
    
    def _extract_price(self, query: str) -> Dict[str, Any]:
        """提取价格信息"""
        params = {}
        
        # 提取价格范围关键词
        for budget_level, keywords in self.budget_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    if budget_level == 'low':
                        params['min_price'] = 0
                        params['max_price'] = 20
                    elif budget_level == 'medium':
                        params['min_price'] = 15
                        params['max_price'] = 35
                    elif budget_level == 'high':
                        params['min_price'] = 30
                        params['max_price'] = 100
                    break
        
        # 提取具体价格数字
        price_pattern = r'(\d+)[元块]'
        prices = re.findall(price_pattern, query)
        
        if len(prices) == 1:
            # 单个价格：作为最高价格
            price = int(prices[0])
            if 'max_price' not in params or price < params['max_price']:
                params['max_price'] = price
        elif len(prices) >= 2:
            # 两个价格：作为价格范围
            price1, price2 = int(prices[0]), int(prices[1])
            params['min_price'] = min(price1, price2)
            params['max_price'] = max(price1, price2)
        
        return params
    
    def _extract_dish_name(self, query: str) -> str:
        """提取具体菜品名称"""
        # 常见的菜品名称关键词
        dish_keywords = [
            '牛肉面', '拉面', '刀削面', '炒饭', '盖饭', '水饺', '蒸饺',
            '汤', '粥', '凉菜', '热菜', '小吃', '套餐'
        ]
        
        for dish in dish_keywords:
            if dish in query:
                return dish
        
        return ""
    
    def get_extraction_summary(self, user_query: str) -> Dict[str, Any]:
        """
        获取关键词提取的详细摘要
        
        Args:
            user_query: 用户查询
            
        Returns:
            提取摘要
        """
        params = self.extract(user_query)
        
        return {
            "original_query": user_query,
            "extracted_params": params,
            "intent_detected": bool(params),  # 是否有明确的查询意图
            "confidence": self._calculate_confidence(params)
        }
    
    def _calculate_confidence(self, params: Dict) -> float:
        """计算提取置信度"""
        if not params:
            return 0.0
        
        # 简单的置信度计算：基于提取到的参数数量
        param_count = len(params)
        base_confidence = min(param_count / 5.0, 1.0)  # 最多5个参数
        
        # 如果有具体菜品名称，置信度更高
        if params.get('name'):
            base_confidence += 0.2
        
        # 如果有明确的价格范围，置信度更高
        if params.get('min_price') and params.get('max_price'):
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)


# 创建全局实例
keyword_extractor = KeywordExtractor()
