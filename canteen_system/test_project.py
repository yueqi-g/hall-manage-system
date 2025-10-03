#!/usr/bin/env python
"""
食堂管理系统项目测试脚本
用于检测项目是否能正常运行
"""

import os
import sys
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_system.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from canteen.models import Merchant, Dish, UserPreference, Order, OrderItem, FootTraffic

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    try:
        # 测试基本查询
        merchant_count = Merchant.objects.count()
        dish_count = Dish.objects.count()
        print(f"✅ 数据库连接正常")
        print(f"   - 商家数量: {merchant_count}")
        print(f"   - 菜品数量: {dish_count}")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_model_creation():
    """测试模型创建"""
    print("\n🔍 测试模型创建...")
    try:
        # 创建测试商家
        merchant = Merchant.objects.create(
            name="测试商家",
            hall="第一食堂",
            location="窗口1",
            contact_info="12345678901",
            description="这是一个测试商家"
        )
        
        # 创建测试菜品
        dish = Dish.objects.create(
            merchant=merchant,
            name="测试菜品",
            description="这是一个测试菜品",
            price=15.50,
            category="饭",
            taste="辣",
            spice_level=2
        )
        
        print(f"✅ 模型创建成功")
        print(f"   - 创建商家: {merchant}")
        print(f"   - 创建菜品: {dish}")
        
        # 清理测试数据
        dish.delete()
        merchant.delete()
        return True
    except Exception as e:
        print(f"❌ 模型创建失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点"""
    print("\n🔍 测试API端点...")
    client = Client()
    
    # 测试的API端点
    endpoints = [
        '/api/merchants/',
        '/api/dishes/',
        '/api/user-preferences/',
        '/api/orders/',
        '/api/foot-traffic/',
        '/admin/',
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            response = client.get(endpoint)
            if response.status_code in [200, 401, 403, 302]:  # 401/403/302 也是正常的（需要认证或重定向）
                results[endpoint] = f"✅ {response.status_code}"
            else:
                results[endpoint] = f"⚠️ {response.status_code}"
        except Exception as e:
            results[endpoint] = f"❌ 错误: {str(e)}"
    
    print("API端点测试结果:")
    for endpoint, result in results.items():
        print(f"   {endpoint}: {result}")
    
    return all("✅" in result for result in results.values())

def test_ai_services():
    """测试AI服务端点"""
    print("\n🔍 测试AI服务...")
    client = Client()
    
    try:
        # 测试菜品推荐
        response = client.post('/api/ai-services/recommend_dishes/', 
                             json.dumps({
                                 'categories': ['饭'],
                                 'tastes': ['辣'],
                                 'max_price': 20.00,
                                 'max_results': 3
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ AI菜品推荐服务正常")
            data = response.json()
            print(f"   - 推荐数量: {data.get('recommendation_count', 0)}")
        else:
            print(f"⚠️ AI菜品推荐服务返回状态码: {response.status_code}")
        
        # 测试客流量预测
        response = client.post('/api/ai-services/predict_traffic/',
                             json.dumps({
                                 'merchant_id': 1,
                                 'date': '2024-01-15',
                                 'time_slot': '午餐'
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ AI客流量预测服务正常")
            data = response.json()
            print(f"   - 预测客流量: {data.get('predicted_traffic', 0)}")
        else:
            print(f"⚠️ AI客流量预测服务返回状态码: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ AI服务测试失败: {e}")
        return False

def test_server_startup():
    """测试服务器启动"""
    print("\n🔍 测试服务器启动...")
    try:
        # 这里只是检查配置，不实际启动服务器
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        print("✅ WSGI应用创建成功")
        return True
    except Exception as e:
        print(f"❌ 服务器启动测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始检测食堂管理系统项目...")
    print("=" * 50)
    
    tests = [
        ("数据库连接", test_database_connection),
        ("模型创建", test_model_creation),
        ("API端点", test_api_endpoints),
        ("AI服务", test_ai_services),
        ("服务器启动", test_server_startup),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{len(results)} 项测试通过")
    
    if passed == len(results):
        print("🎉 恭喜！项目可以正常运行！")
        return True
    else:
        print("⚠️ 项目存在问题，请检查失败的测试项")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
