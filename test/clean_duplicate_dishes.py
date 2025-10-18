"""
清理数据库中的重复菜品
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


def clean_duplicate_dishes():
    """清理重复菜品"""
    dish_repo = DishRepository()
    
    # 获取所有菜品
    all_dishes = dish_repo.filter_dishes({})
    print(f'数据库中共有 {len(all_dishes)} 个菜品')
    
    # 按名称、价格、商家分组统计
    dish_groups = {}
    for dish in all_dishes:
        key = (dish['name'], dish['price'], dish.get('store_name', '未知'))
        if key in dish_groups:
            dish_groups[key].append(dish)
        else:
            dish_groups[key] = [dish]
    
    # 找出重复的菜品
    duplicates_to_remove = []
    for key, dish_list in dish_groups.items():
        if len(dish_list) > 1:
            print(f'发现重复菜品: {key[0]} - ¥{key[1]} - {key[2]} (重复 {len(dish_list)} 次)')
            # 保留第一个，删除其他的
            for dish in dish_list[1:]:
                duplicates_to_remove.append(dish['id'])
                print(f'  将删除 ID: {dish["id"]}')
    
    if not duplicates_to_remove:
        print("没有发现需要删除的重复菜品")
        return
    
    # 确认删除
    print(f'\n将要删除 {len(duplicates_to_remove)} 个重复菜品')
    confirm = input("确认删除？(y/N): ")
    
    if confirm.lower() == 'y':
        deleted_count = 0
        for dish_id in duplicates_to_remove:
            try:
                result = dish_repo.delete_dish(dish_id)
                if result:
                    print(f'✓ 删除菜品 ID: {dish_id}')
                    deleted_count += 1
                else:
                    print(f'✗ 删除失败 ID: {dish_id}')
            except Exception as e:
                print(f'✗ 删除出错 ID: {dish_id}: {str(e)}')
        
        print(f'\n删除完成！共删除了 {deleted_count} 个重复菜品')
        
        # 验证删除结果
        remaining_dishes = dish_repo.filter_dishes({})
        print(f'删除后数据库中共有 {len(remaining_dishes)} 个菜品')
    else:
        print("取消删除操作")


if __name__ == "__main__":
    clean_duplicate_dishes()
