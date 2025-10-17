#!/usr/bin/env python
"""
菜品筛选功能测试脚本
用于测试新增的价格范围、辣度等级、人流量等筛选功能
"""

import requests
import json
from typing import Dict, Any

# API基础URL
BASE_URL = "http://localhost:8000/api"


def print_response(response: requests.Response, title: str):
    """打印API响应"""
    print(f"\n{'='*60}")
    print(f"测试: {title}")
    print(f"{'='*60}")
    print(f"状态码: {response.status_code}")
    
    try:
        data = response.json()
        print(f"响应数据:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        
        if data.get('success') and 'data' in data:
            dishes = data['data'].get('dishes', [])
            print(f"\n找到 {len(dishes)} 个菜品:")
            for dish in dishes[:5]:  # 只显示前5个
                print(f"  - {dish.get('name')} | ¥{dish.get('price')} | "
                      f"辣度: {dish.get('spice_level', 'N/A')} | "
                      f"食堂: {dish.get('canteen', 'N/A')}")
            if len(dishes) > 5:
                print(f"  ... 还有 {len(dishes) - 5} 个菜品")
    except Exception as e:
        print(f"解析响应失败: {e}")
        print(response.text)


def test_price_range_filter():
    """测试价格范围筛选"""
    url = f"{BASE_URL}/dishes/filter"
    params = {
        'price_min': 10,
        'price_max': 30
    }
    response = requests.get(url, params=params)
    print_response(response, "价格范围筛选 (¥10-¥30)")


def test_spice_level_filter():
    """测试辣度等级筛选"""
    url = f"{BASE_URL}/dishes/filter"
    params = {
        'spice_level': 3
    }
    response = requests.get(url, params=params)
    print_response(response, "辣度等级筛选 (辣度 ≤ 3)")


def test_crowd_level_filter():
    """测试人流量筛选"""
    url = f"{BASE_URL}/dishes/filter"
    params = {
        'crowd_level': 'low'
    }
    response = requests.get(url, params=params)
    print_response(response, "人流量筛选 (人少)")


def test_hall_filter():
    """测试食堂筛选"""
    url = f"{BASE_URL}/dishes/filter"
    params = {
        'hall': '第一食堂'
    }
    response = requests.get(url, params=params)
    print_response(response, "食堂筛选 (第一食堂)")


def test_combined_filter():
    """测试组合筛选"""
    url = f"{BASE_URL}/dishes/filter"
    params = {
        'price_min': 15,
        'price_max': 25,
        'spice_level': 2,
        'hall': '第二食堂',
        'ordering': 'price'
    }
    response = requests.get(url, params=params)
    print_response(response, "组合筛选 (价格¥15-¥25, 辣度≤2, 第二食堂, 按价格排序)")


def test_sorting():
    """测试排序功能"""
    url = f"{BASE_URL}/dishes/filter"
    
    # 测试按价格升序
    params = {'ordering': 'price'}
    response = requests.get(url, params=params)
    print_response(response, "按价格升序排序")
    
    # 测试按价格降序
    params = {'ordering': '-price'}
    response = requests.get(url, params=params)
    print_response(response, "按价格降序排序")
    
    # 测试按评分降序
    params = {'ordering': '-rating'}
    response = requests.get(url, params=params)
    print_response(response, "按评分降序排序")


def test_keyword_search_with_filters():
    """测试关键词搜索带筛选"""
    url = f"{BASE_URL}/dishes/search"
    params = {
        'q': '面',
        'price_min': 10,
        'price_max': 20,
        'spice_level': 3,
        'ordering': 'price'
    }
    response = requests.get(url, params=params)
    print_response(response, "关键词搜索带筛选 (搜索'面', 价格¥10-¥20, 辣度≤3)")


def test_edge_cases():
    """测试边界情况"""
    url = f"{BASE_URL}/dishes/filter"
    
    # 测试无筛选条件
    response = requests.get(url)
    print_response(response, "无筛选条件（返回所有菜品）")
    
    # 测试空值筛选
    params = {
        'price_min': '',
        'price_max': '',
        'spice_level': '',
        'crowd_level': 'any',
        'hall': ''
    }
    response = requests.get(url, params=params)
    print_response(response, "空值筛选（应忽略空值）")
    
    # 测试不存在的食堂
    params = {'hall': '不存在的食堂'}
    response = requests.get(url, params=params)
    print_response(response, "不存在的食堂（应返回空结果）")


def main():
    """运行所有测试"""
    print("="*60)
    print("菜品筛选功能测试")
    print("="*60)
    print("\n确保后端服务已启动: python manage.py runserver")
    print("\n开始测试...\n")
    
    try:
        # 基础筛选测试
        test_price_range_filter()
        test_spice_level_filter()
        test_crowd_level_filter()
        test_hall_filter()
        
        # 组合筛选测试
        test_combined_filter()
        
        # 排序测试
        test_sorting()
        
        # 关键词搜索测试
        test_keyword_search_with_filters()
        
        # 边界情况测试
        test_edge_cases()
        
        print("\n" + "="*60)
        print("测试完成！")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n[错误] 无法连接到后端服务")
        print("请确保后端服务已启动: python manage.py runserver")
    except Exception as e:
        print(f"\n[错误] 测试失败: {e}")


if __name__ == "__main__":
    main()


