"""
天气API测试脚本
测试天气API的连接和功能
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ai.context_service import ContextService

def test_weather_api_connection():
    """测试天气API连接"""
    print("=== 天气API测试 ===")
    
    # 检查API密钥
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        print("❌ 未设置WEATHER_API_KEY环境变量")
        print("请设置环境变量：export WEATHER_API_KEY=您的API密钥")
        return False
    
    print(f"✅ 已设置天气API密钥: {api_key[:10]}...")
    
    # 测试天气服务
    service = ContextService()
    weather_info = service.get_weather_info()
    
    if weather_info.get('weather') != '未知':
        print(f"✅ 天气API连接成功！")
        print(f"当前天气: {weather_info['weather']}，温度: {weather_info['temperature']}°C")
        print(f"季节: {weather_info['season']}，湿度: {weather_info['humidity']}%")
        print(f"风力等级: {weather_info['wind_level']}")
        return True
    else:
        print("❌ 天气API连接失败")
        return False

def test_context_service():
    """测试完整的情景数据服务"""
    print("\n=== 完整情景数据测试 ===")
    
    service = ContextService()
    
    # 测试节日信息
    import datetime
    today = datetime.date.today()
    festival_info = service.get_situational_festival_info(today)
    print(f"今天({today})的节日标签: {festival_info}")
    
    # 测试天气信息
    weather_info = service.get_weather_info()
    print(f"天气信息: {weather_info}")
    
    # 测试客流量信息
    crowd_info = service.get_crowd_info()
    print(f"客流量信息: {crowd_info}")
    
    # 测试所有情景数据
    context_data = service.get_all_context_data()
    print(f"完整情景数据: {context_data}")

def test_weather_impact_on_recommendation():
    """测试天气对推荐的影响"""
    print("\n=== 天气对推荐的影响测试 ===")
    
    service = ContextService()
    weather_info = service.get_weather_info()
    temperature = weather_info['temperature']
    weather_condition = weather_info['weather']
    
    print(f"当前温度: {temperature}°C")
    print(f"当前天气: {weather_condition}")
    
    # 基于天气的推荐逻辑
    if temperature < 15:
        print("❄️ 寒冷天气推荐: 辣味菜品、热汤、火锅等暖身食物")
    elif temperature > 25:
        print("☀️ 炎热天气推荐: 清淡菜品、沙拉、冷饮等清爽食物")
    else:
        print("🌤️ 舒适天气推荐: 各类菜品均可")
    
    if '雨' in weather_condition:
        print("🌧️ 雨天推荐: 热汤、热饮、室内用餐")
    elif '晴' in weather_condition:
        print("☀️ 晴天推荐: 户外用餐、清爽菜品")
    elif '风' in weather_condition:
        print("💨 大风天气推荐: 热食，避免冷食")

def main():
    """主测试函数"""
    print("开始天气API测试...")
    
    # 测试连接
    if not test_weather_api_connection():
        print("\n⚠️ 由于连接失败，将使用备用天气数据")
    
    # 测试完整服务
    test_context_service()
    
    # 测试天气影响
    test_weather_impact_on_recommendation()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
