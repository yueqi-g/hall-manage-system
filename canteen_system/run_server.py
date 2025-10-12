#!/usr/bin/env python
"""
启动Django开发服务器的脚本
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    # 设置Django设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'canteen_system.settings')
    
    # 初始化Django
    django.setup()
    
    # 运行服务器
    print("正在启动食堂管理系统...")
    print("前端访问地址: http://127.0.0.1:8000/")
    print("用户仪表板: http://127.0.0.1:8000/user/")
    print("商家仪表板: http://127.0.0.1:8000/merchant/")
    print("API接口: http://127.0.0.1:8000/api/")
    print("管理后台: http://127.0.0.1:8000/admin/")
    print("按 Ctrl+C 停止服务器")
    
    try:
        execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\n服务器已停止")
