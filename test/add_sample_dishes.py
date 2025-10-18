"""
为数据库添加示例菜品数据
确保AI推荐功能有足够的数据进行测试
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'canteen_new'))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from data.repositories import DishRepository, MerchantRepository


def add_sample_dishes():
    """添加示例菜品数据"""
    print("开始添加示例菜品数据...")
    
    # 创建菜品仓库实例
    dish_repo = DishRepository()
    merchant_repo = MerchantRepository()
    
    # 获取商家列表
    try:
        # 尝试获取所有食堂的商家
        merchants = []
        # 尝试常见的食堂名称
        halls = ['一食堂', '二食堂', '三食堂', '四食堂', '五食堂', '中心食堂']
        for hall in halls:
            hall_merchants = merchant_repo.get_merchants_by_hall(hall)
            merchants.extend(hall_merchants)
        
        if not merchants:
            print("警告：没有找到商家，将使用默认商家ID")
            merchant_id = 1
        else:
            merchant_id = merchants[0]['id']
            print(f"使用商家ID: {merchant_id} - 商家名称: {merchants[0].get('storeName', '未知')}")
    except Exception as e:
        print(f"获取商家时出错: {str(e)}，使用默认商家ID")
        merchant_id = 1
    
    # 示例菜品数据
    sample_dishes = [
        # 面食类 - 辣味
        {
            "name": "重庆小面",
            "price": 18.0,
            "category": "面",
            "taste": "辣",
            "spice_level": 3,
            "rating": 4.6,
            "description": "正宗重庆风味，麻辣鲜香",
            "merchantId": merchant_id
        },
        {
            "name": "麻辣牛肉面",
            "price": 25.0,
            "category": "面",
            "taste": "辣",
            "spice_level": 4,
            "rating": 4.7,
            "description": "牛肉鲜嫩，麻辣过瘾",
            "merchantId": merchant_id
        },
        {
            "name": "酸辣粉",
            "price": 15.0,
            "category": "面",
            "taste": "辣",
            "spice_level": 2,
            "rating": 4.5,
            "description": "酸辣开胃，粉条Q弹",
            "merchantId": merchant_id
        },
        {
            "name": "担担面",
            "price": 20.0,
            "category": "面",
            "taste": "辣",
            "spice_level": 3,
            "rating": 4.6,
            "description": "四川特色，麻辣鲜香",
            "merchantId": merchant_id
        },
        
        # 面食类 - 其他口味
        {
            "name": "番茄鸡蛋面",
            "price": 16.0,
            "category": "面",
            "taste": "淡",
            "spice_level": 0,
            "rating": 4.4,
            "description": "酸甜可口，营养丰富",
            "merchantId": merchant_id
        },
        {
            "name": "炸酱面",
            "price": 22.0,
            "category": "面",
            "taste": "咸",
            "spice_level": 1,
            "rating": 4.5,
            "description": "传统北京风味，酱香浓郁",
            "merchantId": merchant_id
        },
        
        # 饭类 - 辣味
        {
            "name": "麻辣香锅",
            "price": 28.0,
            "category": "饭",
            "taste": "辣",
            "spice_level": 4,
            "rating": 4.8,
            "description": "多种食材，麻辣鲜香",
            "merchantId": merchant_id
        },
        {
            "name": "水煮肉片",
            "price": 32.0,
            "category": "饭",
            "taste": "辣",
            "spice_level": 5,
            "rating": 4.7,
            "description": "麻辣鲜香，肉质鲜嫩",
            "merchantId": merchant_id
        },
        {
            "name": "宫保鸡丁",
            "price": 26.0,
            "category": "饭",
            "taste": "辣",
            "spice_level": 2,
            "rating": 4.6,
            "description": "酸甜微辣，鸡肉鲜嫩",
            "merchantId": merchant_id
        },
        
        # 饭类 - 其他口味
        {
            "name": "红烧肉",
            "price": 30.0,
            "category": "饭",
            "taste": "咸",
            "spice_level": 0,
            "rating": 4.7,
            "description": "肥而不腻，入口即化",
            "merchantId": merchant_id
        },
        {
            "name": "糖醋里脊",
            "price": 24.0,
            "category": "饭",
            "taste": "酸甜",
            "spice_level": 0,
            "rating": 4.5,
            "description": "外酥里嫩，酸甜可口",
            "merchantId": merchant_id
        },
        {
            "name": "清炒时蔬",
            "price": 18.0,
            "category": "饭",
            "taste": "淡",
            "spice_level": 0,
            "rating": 4.3,
            "description": "清淡健康，营养均衡",
            "merchantId": merchant_id
        },
        
        # 饺子类
        {
            "name": "猪肉白菜饺子",
            "price": 20.0,
            "category": "饺子",
            "taste": "咸",
            "spice_level": 0,
            "rating": 4.4,
            "description": "传统口味，皮薄馅大",
            "merchantId": merchant_id
        },
        {
            "name": "韭菜猪肉饺子",
            "price": 22.0,
            "category": "饺子",
            "taste": "咸",
            "spice_level": 0,
            "rating": 4.5,
            "description": "韭菜鲜香，猪肉鲜美",
            "merchantId": merchant_id
        },
        {
            "name": "三鲜饺子",
            "price": 25.0,
            "category": "饺子",
            "taste": "咸",
            "spice_level": 0,
            "rating": 4.6,
            "description": "虾仁、猪肉、蔬菜，鲜美可口",
            "merchantId": merchant_id
        },
        
        # 其他分类
        {
            "name": "酸菜鱼",
            "price": 35.0,
            "category": "其他",
            "taste": "辣",
            "spice_level": 3,
            "rating": 4.7,
            "description": "酸辣开胃，鱼肉鲜嫩",
            "merchantId": merchant_id
        },
        {
            "name": "麻婆豆腐",
            "price": 18.0,
            "category": "其他",
            "taste": "辣",
            "spice_level": 4,
            "rating": 4.6,
            "description": "麻辣鲜香，豆腐嫩滑",
            "merchantId": merchant_id
        },
        {
            "name": "清蒸鲈鱼",
            "price": 38.0,
            "category": "其他",
            "taste": "淡",
            "spice_level": 0,
            "rating": 4.5,
            "description": "鲜嫩可口，原汁原味",
            "merchantId": merchant_id
        }
    ]
    
    # 添加菜品
    added_count = 0
    for dish_data in sample_dishes:
        try:
            result = dish_repo.create_dish(dish_data)
            if result:
                print(f"✓ 添加菜品: {dish_data['name']} - ¥{dish_data['price']} - {dish_data['category']} - {dish_data['taste']}")
                added_count += 1
            else:
                print(f"✗ 添加失败: {dish_data['name']}")
        except Exception as e:
            print(f"✗ 添加菜品时出错: {dish_data['name']} - {str(e)}")
    
    print(f"\n添加完成！共添加了 {added_count} 个菜品")
    
    # 验证添加结果
    print("\n验证菜品数据...")
    # 使用filter_dishes方法获取所有菜品
    all_dishes = dish_repo.filter_dishes({})
    print(f"数据库中共有 {len(all_dishes)} 个菜品")
    
    # 按分类统计
    categories = {}
    for dish in all_dishes:
        category = dish.get('category', '未知')
        categories[category] = categories.get(category, 0) + 1
    
    print("菜品分类统计:")
    for category, count in categories.items():
        print(f"  {category}: {count} 个")
    
    # 按口味统计
    tastes = {}
    for dish in all_dishes:
        taste = dish.get('taste', '未知')
        tastes[taste] = tastes.get(taste, 0) + 1
    
    print("菜品口味统计:")
    for taste, count in tastes.items():
        print(f"  {taste}: {count} 个")


if __name__ == "__main__":
    add_sample_dishes()
