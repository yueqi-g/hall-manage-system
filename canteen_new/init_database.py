#!/usr/bin/env python
"""
数据库初始化脚本
运行此脚本初始化数据库表结构和示例数据
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from data.database_init import DatabaseInitializer

def main():
    """主函数"""
    print("="*50)
    print("食堂管理系统 - 数据库初始化")
    print("="*50)
    print()
    
    # 创建初始化器
    db_init = DatabaseInitializer()
    
    # 初始化数据库
    print("开始初始化数据库...")
    result = db_init.initialize_database()
    
    if result['success']:
        print("\n✅ 数据库初始化成功！")
        print("\n创建的表:")
        for table in result['tables_created']:
            print(f"  - {table}")
        
        if result['sample_data']:
            print("\n已创建示例数据:")
            print("  - 示例商家账号")
            print("  - 示例菜品数据")
        
        print("\n" + "="*50)
        print("你现在可以启动服务器并测试功能了！")
        print("="*50)
    else:
        print("\n❌ 数据库初始化失败！")
        print(f"错误: {result.get('error', '未知错误')}")
        sys.exit(1)

if __name__ == '__main__':
    main()

