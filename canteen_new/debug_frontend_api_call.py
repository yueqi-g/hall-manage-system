"""
前端API调用详细调试脚本
模拟前端调用API并显示完整的LLM调用过程
"""
import os
import sys
import django
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ai.services import ai_recommendation_service


def debug_frontend_api_call():
    """调试前端API调用过程"""
    print("=== 前端API调用详细调试 ===")
    
    # 模拟前端调用
    test_queries = [
        "推荐一些辣的菜品",
        "想吃点暖和的",
        "有什么便宜的菜品推荐吗？"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"测试查询: '{query}'")
        print(f"{'='*50}")
        
        try:
            # 直接调用AI服务
            result = ai_recommendation_service.process_user_query(query)
            
            print(f"\n=== 最终结果 ===")
            print(f"结果类型: {result.get('type')}")
            print(f"内容: {result.get('content')}")
            print(f"菜品数量: {len(result.get('dishes', []))}")
            print(f"推荐理由数量: {len(result.get('reasons', []))}")
            
            # 显示前几个菜品
            dishes = result.get('dishes', [])
            if dishes:
                print(f"\n=== 推荐菜品 ===")
                for i, dish in enumerate(dishes[:3]):
                    print(f"{i+1}. {dish.get('name')} - ¥{dish.get('price')} - {dish.get('taste')}")
            
        except Exception as e:
            print(f"❌ 调用失败: {e}")
            import traceback
            traceback.print_exc()


def debug_context_aware_api_call():
    """调试基于情景数据的API调用"""
    print(f"\n{'='*50}")
    print("测试基于情景数据的API调用")
    print(f"{'='*50}")
    
    query = "想吃点暖和的"
    user_id = 1  # 测试用户ID
    
    try:
        result = ai_recommendation_service.process_user_query_with_context(query, user_id)
        
        print(f"\n=== 基于情景数据的最终结果 ===")
        print(f"结果类型: {result.get('type')}")
        print(f"内容: {result.get('content')}")
        print(f"菜品数量: {len(result.get('dishes', []))}")
        
        # 显示情景数据
        context_data = result.get('context_data', {})
        if context_data:
            print(f"\n=== 情景数据 ===")
            print(f"日期: {context_data.get('date_info', {}).get('current_date')}")
            print(f"天气: {context_data.get('weather_info', {}).get('weather')}")
            print(f"温度: {context_data.get('weather_info', {}).get('temperature')}°C")
            print(f"客流: {context_data.get('crowd_info', {}).get('crowd_level')}")
        
    except Exception as e:
        print(f"❌ 基于情景数据的调用失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("开始前端API调用调试...")
    debug_frontend_api_call()
    debug_context_aware_api_call()
    print("\n调试完成！")
