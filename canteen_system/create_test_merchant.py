#!/usr/bin/env python
"""
创建测试商家账号的脚本
使用方法: python create_test_merchant.py
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_system.settings')
django.setup()

from django.contrib.auth.models import User
from canteen.models import Merchant

def create_test_merchant():
    """创建测试商家账号和商家记录"""
    
    # 测试商家信息
    username = 'testmerchant'
    password = '123456'
    email = 'testmerchant@example.com'
    merchant_name = 'testmerchant'
    hall = '一食堂'
    location = '窗口1'
    
    print('=' * 50)
    print('创建测试商家账号')
    print('=' * 50)
    
    # 检查用户是否已存在
    user = User.objects.filter(username=username).first()
    if user:
        print(f'✓ 用户 {username} 已存在')
    else:
        # 创建用户
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        print(f'✓ 创建用户: {username}')
    
    # 检查商家记录是否已存在
    merchant = Merchant.objects.filter(name=merchant_name).first()
    if merchant:
        print(f'✓ 商家记录 {merchant_name} 已存在 (ID: {merchant.id})')
        # 确保用户关联到商家
        if merchant.user != user:
            merchant.user = user
            merchant.save()
            print(f'✓ 已关联用户到商家记录')
    else:
        # 创建商家记录
        merchant = Merchant.objects.create(
            user=user,
            name=merchant_name,
            hall=hall,
            location=location,
            description='测试商家账号',
            status=True
        )
        print(f'✓ 创建商家记录: {merchant_name} (ID: {merchant.id})')
    
    print('\n' + '=' * 50)
    print('测试商家账号信息:')
    print('=' * 50)
    print(f'用户名: {username}')
    print(f'密码: {password}')
    print(f'商家ID: {merchant.id}')
    print(f'商家名称: {merchant.name}')
    print(f'食堂: {merchant.hall}')
    print(f'窗口: {merchant.location}')
    print('=' * 50)
    print('\n✓ 测试商家账号创建完成！')
    print('\n现在可以使用以下信息登录:')
    print(f'  用户名: {username}')
    print(f'  密码: {password}')
    print('\n登录后即可在商家仪表板添加菜品。')

if __name__ == '__main__':
    try:
        create_test_merchant()
    except Exception as e:
        print(f'\n✗ 错误: {str(e)}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

