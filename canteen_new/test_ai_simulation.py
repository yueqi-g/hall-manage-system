"""
AI推荐功能模拟测试脚本
测试AI推荐服务的逻辑，不依赖数据库
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_ai_logic():
    """测试AI推荐逻辑（不依赖数据库）"""
    print("=" * 50)
    print("AI推荐逻辑测试（模拟数据）")
    print("=" * 50)
    
    # 模拟AI推荐服务
    class MockAIRecommendationService:
        def process_user_query(self, user_query: str, user_preferences: dict = None):
            """模拟处理用户查询"""
            query_lower = user_query.lower()
            
            # 检查是否需要调用工具函数
            should_call_tool = any(keyword in query_lower for keyword in [
                '推荐', '想吃', '找', '搜索', '查询', '辣', '咸', '淡', '酸甜',
                '价格', '评分', '面', '饭', '饺子', '菜品', '菜'
            ])
            
            if should_call_tool:
                # 模拟工具函数调用和菜品查询
                tool_args = self.extract_parameters_from_query(user_query)
                print(f"提取的参数: {tool_args}")
                
                # 模拟菜品数据
                mock_dishes = [
                    {"name": "麻辣香锅", "price": 28, "taste": "辣", "rating": 4.8, "category": "饭"},
                    {"name": "重庆小面", "price": 18, "taste": "辣", "rating": 4.6, "category": "面"},
                    {"name": "红烧肉", "price": 25, "taste": "咸", "rating": 4.7, "category": "饭"},
                    {"name": "番茄鸡蛋面", "price": 15, "taste": "淡", "rating": 4.5, "category": "面"},
                    {"name": "糖醋里脊", "price": 22, "taste": "酸甜", "rating": 4.6, "category": "饭"}
                ]
                
                # 应用筛选条件
                filtered_dishes = self.apply_filters(mock_dishes, tool_args)
                
                return self.format_recommendation_response(filtered_dishes, user_query)
            else:
                # 模拟直接回复
                return {
                    "type": "chat_response",
                    "content": "我是食堂菜品推荐助手，请问您想吃什么类型的菜品？我可以帮您推荐。",
                    "dishes": []
                }
        
        def extract_parameters_from_query(self, user_query: str):
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
            
            # 提取价格范围
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
        
        def apply_filters(self, dishes, criteria):
            """应用筛选条件"""
            filtered = dishes.copy()
            
            # 分类筛选
            if criteria.get('category'):
                filtered = [d for d in filtered if d.get('category') == criteria['category']]
            
            # 口味筛选
            if criteria.get('taste'):
                filtered = [d for d in filtered if d.get('taste') == criteria['taste']]
            
            # 价格筛选
            if criteria.get('min_price'):
                filtered = [d for d in filtered if d.get('price', 0) >= criteria['min_price']]
            if criteria.get('max_price'):
                filtered = [d for d in filtered if d.get('price', 0) <= criteria['max_price']]
            
            # 数量限制
            if criteria.get('limit'):
                filtered = filtered[:criteria['limit']]
            
            return filtered
        
        def format_recommendation_response(self, dishes, user_query):
            """格式化推荐结果"""
            if not dishes:
                return {
                    "type": "recommendation",
                    "content": f"根据您的需求'{user_query}'，没有找到符合条件的菜品。",
                    "dishes": [],
                    "query_analysis": {"intent": "菜品查询"}
                }
            
            return {
                "type": "recommendation",
                "content": f"根据您的需求'{user_query}'，为您推荐以下{len(dishes)}个菜品：",
                "dishes": dishes,
                "reasons": ["符合您的搜索条件"] * len(dishes),
                "query_analysis": {"intent": "菜品查询"}
            }
    
    # 创建模拟服务实例
    mock_service = MockAIRecommendationService()
    
    # 测试场景
    test_cases = [
        {
            "name": "明确查询 - 辣的面食",
            "query": "我想吃辣的面食，价格在20元以内"
        },
        {
            "name": "模糊查询 - 推荐好吃的",
            "query": "推荐一些好吃的"
        },
        {
            "name": "闲聊 - 天气",
            "query": "今天天气怎么样"
        },
        {
            "name": "具体价格查询",
            "query": "价格15-25元的菜品"
        },
        {
            "name": "口味偏好查询",
            "query": "推荐咸味的饭"
        },
        {
            "name": "边界测试 - 特辣",
            "query": "特辣的菜品"
        },
        {
            "name": "错误参数测试",
            "query": "分类为火锅的菜品"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case['name']}")
        print(f"查询: {test_case['query']}")
        print("-" * 30)
        
        try:
            # 调用模拟服务
            result = mock_service.process_user_query(test_case['query'])
            
            # 输出结果
            print(f"响应类型: {result.get('type')}")
            print(f"内容: {result.get('content')}")
            
            if result.get('dishes'):
                print(f"推荐菜品数量: {len(result.get('dishes'))}")
                for j, dish in enumerate(result.get('dishes')[:3], 1):
                    print(f"  {j}. {dish.get('name')} - ¥{dish.get('price')} - {dish.get('taste')}")
            
            if result.get('reasons'):
                print("推荐理由:")
                for j, reason in enumerate(result.get('reasons')[:3], 1):
                    print(f"  {j}. {reason}")
            
            if result.get('query_analysis'):
                print(f"查询分析: {result.get('query_analysis')}")
                
        except Exception as e:
            print(f"测试失败: {str(e)}")
    
    print("\n" + "=" * 50)
    print("模拟测试完成")
    print("=" * 50)


if __name__ == "__main__":
    test_ai_logic()
