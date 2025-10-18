"""
基于情景数据的AI推荐功能测试
"""
import sys
import os
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai.services import AIRecommendationService


def test_context_ai():
    """测试基于情景数据的AI推荐功能"""
    print('=== 测试基于情景数据的AI推荐功能 ===')
    service = AIRecommendationService()

    # 测试基于情景数据的推荐
    test_queries = [
        '想吃点暖和的',
        '推荐点出餐快的', 
        '今天有什么特色菜',
        '想吃点清淡的'
    ]

    for query in test_queries:
        print(f'\n查询: {query}')
        result = service.process_user_query_with_context(query, user_id=1)
        print(f'响应类型: {result.get("type")}')
        print(f'内容: {result.get("content")}')
        if result.get('context_data'):
            print(f'情景数据: {result.get("context_data")["date_info"]["festival_tags"]}')
        print('---')


if __name__ == "__main__":
    test_context_ai()
