"""
前端API调用调试脚本
模拟前端调用API并检查是否使用真实LLM
"""
import os
import sys
import django
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from rest_framework.test import APIClient
from rest_framework import status


def test_frontend_api_calls():
    """测试前端API调用是否使用真实LLM"""
    print("=== 前端API调用调试 ===")
    
    client = APIClient()
    
    # 测试1: 普通AI推荐
    print("\n1. 测试普通AI推荐API...")
    response = client.post(
        '/api/dishes/ai-recommend',
        data={
            'query': '推荐一些辣的菜品',
            'preferences': {
                'flavors': ['辣'],
                'budget': {'min': 0, 'max': 50},
                'dietary': []
            }
        },
        format='json'
    )
    
    print(f"响应状态码: {response.status_code}")
