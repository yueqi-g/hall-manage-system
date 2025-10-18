"""
增强AI功能测试脚本
测试真实LLM集成和用户收藏分析
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ai.llm_service import llm_service
from ai.context_service import ContextService
from data.services import dish_service


def test_llm_service():
    """测试LLM服务"""
    print("=== LLM服务测试 ===")
    
    # 测试用户偏好分析
    print("\n1. 测试用户偏好分析...")
    user_prefs = llm_service.get_user_preferences_summary(1)
    print(f"用户偏好: {user_prefs}")
    
    # 测试LLM调用
    print("\n2. 测试LLM调用...")
    messages = [
        {"role": "system", "content": "你是一个食堂菜品推荐助手。"},
        {"role": "user", "content": "推荐一些辣的菜品"}
    ]
    
    response = llm_service.call_llm_with_tools(
        messages=messages,
        tools=[llm_service._extract_parameters_from_query.__globals__['GET_DISHES_SCHEMA']]
    )
    
    print(f"LLM响应类型: {type(response)}")
    
    # 检查是否有工具调用
    if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
        print("检测到工具函数调用")
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"工具函数: {tool_call.function.name}")
        print(f"参数: {tool_call.function.arguments}")
    else:
        print("直接回复:", response.choices[0].message.content)


def test_user_favorites_analysis():
    """测试用户收藏分析"""
    print("\n=== 用户收藏分析测试 ===")
    
    # 测试用户收藏汇总
    print("1. 测试用户收藏汇总...")
    try:
        favorites_summary = dish_service.get_user_favorites_summary(1)
        print(f"收藏汇总: {favorites_summary}")
        
        # 测试偏好推断
        print(f"偏好类别: {favorites_summary.get('preferred_categories', [])}")
        print(f"偏好口味: {favorites_summary.get('preferred_tastes', [])}")
        print(f"预算范围: {favorites_summary.get('budget_range', [])}")
        print(f"辣度耐受: {favorites_summary.get('spice_tolerance', '')}")
        print(f"收藏菜品: {favorites_summary.get('favorite_dishes', [])}")
        print(f"总收藏数: {favorites_summary.get('total_favorites', 0)}")
        
    except Exception as e:
        print(f"收藏分析失败: {e}")


def test_context_integration():
    """测试情景数据集成"""
    print("\n=== 情景数据集成测试 ===")
    
    context_service = ContextService()
    
    # 测试完整情景数据
    print("1. 测试完整情景数据...")
    context_data = context_service.get_all_context_data(1)
    print(f"日期信息: {context_data['date_info']}")
    print(f"天气信息: {context_data['weather_info']}")
    print(f"客流信息: {context_data['crowd_info']}")
    print(f"用户偏好: {context_data['user_preferences']}")
    
    # 测试基于情景的推荐
    print("\n2. 测试基于情景的推荐...")
    user_query = "想吃点暖和的"
    
    # 构建系统提示
    system_prompt = f"""
你是一个智能食堂菜品推荐助手。请结合以下情景因素进行推理推荐：

当前情景：
- 日期：{context_data['date_info']['current_date']}
- 节日/情景标签：{', '.join(context_data['date_info']['festival_tags'])}
- 季节：{context_data['date_info']['current_season']}，{'周末' if context_data['date_info']['is_weekend'] else '工作日'}
- 天气：{context_data['weather_info']['weather']}，温度：{context_data['weather_info']['temperature']}°C
- 客流：{context_data['crowd_info']['crowd_level']}，平均等待时间：{context_data['crowd_info']['avg_wait_time']}分钟
- 用户偏好：{context_data['user_preferences'].get('preferred_categories', [])}类别，{context_data['user_preferences'].get('preferred_tastes', [])}口味

请根据用户需求，调用合适的工具函数查询菜品。
"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    
    response = llm_service.call_llm_with_tools(
        messages=messages,
        tools=[llm_service._extract_parameters_from_query.__globals__['GET_DISHES_SCHEMA']]
    )
    
    print(f"用户查询: {user_query}")
    if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        print(f"工具调用: {tool_call.function.name}")
        print(f"调用参数: {tool_call.function.arguments}")
    else:
        print(f"直接回复: {response.choices[0].message.content}")


def test_llm_config():
    """测试LLM配置"""
    print("\n=== LLM配置测试 ===")
    
    from config.llm_config import llm_config
    
    print(f"提供商: {llm_config.provider}")
    print(f"模型: {llm_config.model}")
    print(f"可用性: {'是' if llm_config.is_available() else '否 (模拟模式)'}")
    print(f"基础URL: {llm_config.base_url}")
    print(f"温度: {llm_config.temperature}")
    print(f"最大token数: {llm_config.max_tokens}")
    
    # 测试配置验证
    if llm_config.validate_config():
        print("配置验证: 通过")
    else:
        print("配置验证: 失败")


def main():
    """主测试函数"""
    print("=== 增强AI功能完整测试 ===")
    
    # 测试LLM配置
    test_llm_config()
    
    # 测试用户收藏分析
    test_user_favorites_analysis()
    
    # 测试LLM服务
    test_llm_service()
    
    # 测试情景数据集成
    test_context_integration()
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    main()
