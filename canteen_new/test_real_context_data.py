"""
测试真实数据源的context_service
验证去除了所有硬编码数据
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ai.context_service import ContextService


def test_real_context_data():
    """测试真实数据源的context_service"""
    print("=== 测试真实数据源的ContextService ===")
    
    service = ContextService()
    
    # 测试节日信息
    print("\n1. 测试节日信息:")
    festival_info = service.get_situational_festival_info()
    print(f"节日标签: {festival_info}")
    
    # 测试天气信息
    print("\n2. 测试天气信息:")
    weather_info = service.get_weather_info()
    print(f"天气信息: {weather_info}")
    if weather_info['weather'] == '未知':
        print("⚠️ 天气API密钥未配置，使用备用数据")
    else:
        print("✅ 使用真实天气数据")
    
    # 测试客流量信息
    print("\n3. 测试客流量信息:")
    crowd_info = service.get_crowd_info()
    print(f"客流量信息: {crowd_info}")
    if crowd_info.get('crowd_level') == '低':
        print("⚠️ 使用估算的客流量数据")
    else:
        print("✅ 使用真实客流量数据")
    
    # 测试用户偏好
    print("\n4. 测试用户偏好:")
    user_prefs = service.get_user_preferences(1)
    print(f"用户偏好: {user_prefs}")
    if user_prefs.get('preferred_categories') == ['饭', '面']:
        print("⚠️ 使用默认用户偏好")
    else:
        print("✅ 使用真实用户偏好数据")
    
    # 测试完整情景数据
    print("\n5. 测试完整情景数据:")
    context_data = service.get_all_context_data(1)
    print(f"完整情景数据:")
    print(f"- 日期: {context_data['date_info']['current_date']}")
    print(f"- 节日: {context_data['date_info']['festival_tags']}")
    print(f"- 季节: {context_data['date_info']['current_season']}")
    print(f"- 天气: {context_data['weather_info']['weather']}")
    print(f"- 温度: {context_data['weather_info']['temperature']}°C")
    print(f"- 客流: {context_data['crowd_info']['crowd_level']}")
    print(f"- 等待时间: {context_data['crowd_info']['avg_wait_time']}分钟")
    print(f"- 用户偏好: {context_data['user_preferences']['preferred_categories']}")
    
    # 验证是否还有硬编码数据
    print("\n6. 验证硬编码数据:")
    has_hardcoded_data = False
    
    # 检查天气数据
    if weather_info['weather'] == '未知' and weather_info['temperature'] == 0:
        print("⚠️ 天气数据使用备用值")
        has_hardcoded_data = True
    
    # 检查客流量数据
    if crowd_info['crowd_level'] == '低' and crowd_info['avg_wait_time'] == 10:
        print("⚠️ 客流量数据使用估算值")
        has_hardcoded_data = True
    
    # 检查用户偏好数据
    if user_prefs['preferred_categories'] == ['饭', '面'] and user_prefs['preferred_tastes'] == ['咸', '辣']:
        print("⚠️ 用户偏好数据使用默认值")
        has_hardcoded_data = True
    
    if not has_hardcoded_data:
        print("✅ 所有数据都来自真实数据源")
    else:
        print("⚠️ 部分数据使用备用值（需要配置API密钥和数据库）")


def test_context_service_with_ai():
    """测试context_service与AI服务的集成"""
    print("\n=== 测试ContextService与AI服务集成 ===")
    
    from ai.services import ai_recommendation_service
    
    # 测试基于情景数据的推荐
    test_queries = [
        "想吃点暖和的",
        "天气热想吃点清爽的",
        "周末想吃点特别的",
        "想吃辣的面食，价格实惠的"
    ]
    
    for query in test_queries:
        print(f"\n测试查询: '{query}'")
        try:
            result = ai_recommendation_service.process_user_query_with_context(query, user_id=1)
            print(f"结果类型: {result.get('type')}")
            print(f"推荐内容: {result.get('content')}")
            print(f"菜品数量: {len(result.get('dishes', []))}")
            
            # 显示使用的情景数据
            context_data = result.get('context_data', {})
            if context_data:
                print(f"使用的情景数据:")
                print(f"- 天气: {context_data.get('weather_info', {}).get('weather')}")
                print(f"- 温度: {context_data.get('weather_info', {}).get('temperature')}°C")
                print(f"- 客流: {context_data.get('crowd_info', {}).get('crowd_level')}")
                print(f"- 季节: {context_data.get('date_info', {}).get('current_season')}")
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    print("开始测试真实数据源的ContextService...")
    test_real_context_data()
    test_context_service_with_ai()
    print("\n测试完成！")
