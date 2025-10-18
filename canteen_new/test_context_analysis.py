"""
测试情景数据分析功能
验证LLM是否真正利用天气、节日等信息进行综合分析
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ai.services import ai_recommendation_service


def test_context_analysis():
    """测试情景数据分析功能"""
    print("=== 情景数据分析测试 ===")
    
    # 测试不同情景下的推荐
    test_cases = [
        {
            "query": "想吃点暖和的",
            "description": "寒冷天气下的暖身推荐"
        },
        {
            "query": "天气热想吃点清爽的", 
            "description": "炎热天气下的清爽推荐"
        },
        {
            "query": "周末想吃点特别的",
            "description": "周末特色推荐"
        },
        {
            "query": "想吃辣的面食，价格实惠的",
            "description": "结合用户需求和情景的综合推荐"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"测试: {test_case['description']}")
        print(f"用户查询: '{test_case['query']}'")
        print(f"{'='*50}")
        
        try:
            # 使用基于情景数据的推荐
            result = ai_recommendation_service.process_user_query_with_context(
                test_case['query'], 
                user_id=1
            )
            
            print(f"\n=== 推荐结果 ===")
            print(f"结果类型: {result.get('type')}")
            print(f"推荐内容: {result.get('content')}")
            print(f"菜品数量: {len(result.get('dishes', []))}")
            
            # 显示情景数据
            context_data = result.get('context_data', {})
            if context_data:
                print(f"\n=== 使用的情景数据 ===")
                print(f"日期: {context_data.get('date_info', {}).get('current_date')}")
                print(f"季节: {context_data.get('date_info', {}).get('current_season')}")
                print(f"节日: {', '.join(context_data.get('date_info', {}).get('festival_tags', []))}")
                print(f"天气: {context_data.get('weather_info', {}).get('weather')}")
                print(f"温度: {context_data.get('weather_info', {}).get('temperature')}°C")
                print(f"客流: {context_data.get('crowd_info', {}).get('crowd_level')}")
            
            # 显示推荐菜品
            dishes = result.get('dishes', [])
            if dishes:
                print(f"\n=== 推荐菜品 ===")
                for i, dish in enumerate(dishes[:5]):
                    print(f"{i+1}. {dish.get('name')} - ¥{dish.get('price')} - {dish.get('taste')} - 评分: {dish.get('rating')}")
            
            # 显示推荐理由
            reasons = result.get('reasons', [])
            if reasons:
                print(f"\n=== 推荐理由 ===")
                for i, reason in enumerate(reasons[:3]):
                    print(f"{i+1}. {reason}")
                    
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()


def analyze_llm_parameters():
    """分析LLM生成的参数是否包含情景推理"""
    print(f"\n{'='*50}")
    print("分析LLM参数中的情景推理")
    print(f"{'='*50}")
    
    query = "想吃点暖和的"
    
    try:
        # 直接调用LLM服务查看参数
        from ai.llm_service import llm_service
        from ai.context_service import ContextService
        
        context_service = ContextService()
        context_data = context_service.get_all_context_data(1)
        
        print(f"当前情景数据:")
        print(f"- 温度: {context_data['weather_info']['temperature']}°C")
        print(f"- 天气: {context_data['weather_info']['weather']}")
        print(f"- 季节: {context_data['date_info']['current_season']}")
        print(f"- 客流: {context_data['crowd_info']['crowd_level']}")
        
        # 构建系统提示
        from ai.services import AIRecommendationService
        ai_service = AIRecommendationService()
        system_prompt = ai_service._build_context_aware_system_prompt(context_data)
        
        print(f"\n系统提示长度: {len(system_prompt)} 字符")
        print(f"系统提示预览: {system_prompt[:200]}...")
        
        # 调用LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
        
        response = llm_service.call_llm_with_tools(
            messages=messages,
            tools=[ai_service._call_context_aware_llm.__globals__['GET_DISHES_SCHEMA']]
        )
        
        print(f"\nLLM响应类型: {type(response)}")
        
        if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            print(f"工具函数: {tool_call.function.name}")
            print(f"参数: {tool_call.function.arguments}")
            
            # 分析参数是否包含情景推理
            import json
            params = json.loads(tool_call.function.arguments)
            print(f"\n参数分析:")
            for key, value in params.items():
                print(f"- {key}: {value}")
                
            # 检查是否包含情景相关参数
            context_params = ['max_wait_time', 'spice_level', 'category', 'taste']
            has_context_reasoning = any(param in params for param in context_params)
            print(f"\n是否包含情景推理: {'✅ 是' if has_context_reasoning else '❌ 否'}")
            
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("开始情景数据分析测试...")
    test_context_analysis()
    analyze_llm_parameters()
    print("\n测试完成！")
