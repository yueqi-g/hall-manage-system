"""
AI推荐功能测试脚本
测试AI推荐服务的各种场景
"""
import sys
import os
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai.services import AIRecommendationService


def test_ai_recommendation():
    """测试AI推荐功能"""
    print("=" * 50)
    print("AI推荐功能测试")
    print("=" * 50)
    
    # 创建AI推荐服务实例
    ai_service = AIRecommendationService()
    
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
            # 调用AI推荐服务
            result = ai_service.process_user_query(test_case['query'])
            
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
    print("测试完成")
    print("=" * 50)


if __name__ == "__main__":
    test_ai_recommendation()
