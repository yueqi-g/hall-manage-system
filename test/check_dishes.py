"""
检查数据库中的菜品数据，排查重复菜品问题
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'canteen_new'))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from data.repositories import DishRepository


def check_duplicate_dishes():
    """检查重复菜品"""
    dish_repo = DishRepository()
    
    # 检查饭类菜品
    print("=== 检查饭类菜品 ===")
    dishes = dish_repo.filter_dishes({'category': '饭'})
    print(f'找到 {len(dishes)} 个饭类菜品:')
    
    # 按名称分组统计
    name_count = {}
    for dish in dishes:
        name = dish['name']
        if name in name_count:
            name_count[name].append(dish)
        else:
            name_count[name] = [dish]
    
    # 显示重复的菜品
    print("\n=== 重复菜品统计 ===")
    for name, dish_list in name_count.items():
        if len(dish_list) > 1:
            print(f'菜品 "{name}" 重复 {len(dish_list)} 次:')
            for dish in dish_list:
                print(f'  ID: {dish["id"]}, 价格: {dish["price"]}, 商家: {dish.get("store_name", "未知")}')
    
    # 显示所有饭类菜品详情
    print("\n=== 所有饭类菜品详情 ===")
    for i, dish in enumerate(dishes):
        print(f'{i+1}. ID: {dish["id"]}, 名称: {dish["name"]}, 价格: {dish["price"]}, 商家: {dish.get("store_name", "未知")}')


if __name__ == "__main__":
    check_duplicate_dishes()
