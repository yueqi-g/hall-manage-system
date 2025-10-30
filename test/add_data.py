"""
为数据库添加完整的示例数据
包括用户、商家、菜品和客流量数据
"""
import sys
import os
import random
from datetime import datetime, timedelta

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'canteen_new'))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from data.repositories import UserRepository, MerchantRepository, DishRepository, OrderRepository
from data.database import execute_update, execute_insert, query_all
from core.security import hash_password


def clear_all_tables():
    """清空所有表数据"""
    print("正在清空所有表数据...")
    
    # 注意删除顺序，避免外键约束
    tables = ['favorites', 'orders', 'traffic_data', 'dishes', 'merchants', 'users']
    
    for table in tables:
        try:
            execute_update(f"DELETE FROM {table}")
            print(f"✓ 已清空 {table} 表")
        except Exception as e:
            print(f"✗ 清空 {table} 表失败: {e}")


def create_sample_users():
    """创建5个示例用户"""
    print("\n正在创建示例用户...")
    
    user_repo = UserRepository()
    users = []
    
    sample_users = [
        {"username": "user1", "email": "user1@example.com", "password": "password123"},
        {"username": "user2", "email": "user2@example.com", "password": "password123"},
        {"username": "user3", "email": "user3@example.com", "password": "password123"},
        {"username": "user4", "email": "user4@example.com", "password": "password123"},
        {"username": "user5", "email": "user5@example.com", "password": "password123"}
    ]
    
    for user_data in sample_users:
        try:
            # 创建用户数据
            user_create_data = {
                "username": user_data["username"],
                "password": hash_password(user_data["password"]),
                "email": user_data["email"],
                "type": "user"
            }
            
            user = user_repo.create_user(user_create_data)
            if user:
                users.append(user)
                print(f"✓ 创建用户: {user_data['username']}")
            else:
                print(f"✗ 创建用户失败: {user_data['username']}")
                
        except Exception as e:
            print(f"✗ 创建用户 {user_data['username']} 时出错: {e}")
    
    return users


def create_sample_merchants():
    """创建10个示例商家"""
    print("\n正在创建示例商家...")
    
    user_repo = UserRepository()
    merchant_repo = MerchantRepository()
    merchants = []
    
    # 食堂分配：一食堂(3个), 二食堂(2个), 三食堂(2个), 四食堂(2个), 其他(1个)
    canteen_distribution = {
        "一食堂": 3,
        "二食堂": 2, 
        "三食堂": 2,
        "四食堂": 2,
        "其他": 1
    }
    
    merchant_data = [
        {"username": "merchant1", "store_name": "川味小厨", "email": "merchant1@example.com"},
        {"username": "merchant2", "store_name": "面面俱到", "email": "merchant2@example.com"},
        {"username": "merchant3", "store_name": "粤式烧腊", "email": "merchant3@example.com"},
        {"username": "merchant4", "store_name": "东北饺子王", "email": "merchant4@example.com"},
        {"username": "merchant5", "store_name": "湘菜馆", "email": "merchant5@example.com"},
        {"username": "merchant6", "store_name": "台湾小吃", "email": "merchant6@example.com"},
        {"username": "merchant7", "store_name": "西北拉面", "email": "merchant7@example.com"},
        {"username": "merchant8", "store_name": "韩式料理", "email": "merchant8@example.com"},
        {"username": "merchant9", "store_name": "日式寿司", "email": "merchant9@example.com"},
        {"username": "merchant10", "store_name": "西式快餐", "email": "merchant10@example.com"}
    ]
    
    canteen_index = 0
    canteens = list(canteen_distribution.keys())
    
    for i, data in enumerate(merchant_data):
        # 分配食堂
        canteen = canteens[canteen_index]
        canteen_distribution[canteen] -= 1
        if canteen_distribution[canteen] == 0:
            canteen_index += 1
        
        try:
            # 先创建用户记录
            user_create_data = {
                "username": data["username"],
                "password": hash_password("merchant123"),
                "email": data["email"],
                "type": "merchant"
            }
            
            user = user_repo.create_user(user_create_data)
            if not user:
                print(f"✗ 创建商家用户失败: {data['username']}")
                continue
            
            # 再创建商家记录
            merchant_create_data = {
                "username": data["username"],
                "storeName": data["store_name"],
                "canteen": canteen,
                "location": f"{canteen} {random.randint(1, 20)}号窗口",
                "contact_info": f"电话: 138-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                "description": f"专业制作{data['store_name']}特色美食，欢迎品尝！"
            }
            
            merchant = merchant_repo.create_merchant(merchant_create_data)
            if merchant:
                merchants.append(merchant)
                print(f"✓ 创建商家: {data['store_name']} ({canteen})")
            else:
                print(f"✗ 创建商家记录失败: {data['store_name']}")
                
        except Exception as e:
            print(f"✗ 创建商家 {data['store_name']} 时出错: {e}")
    
    return merchants


def create_sample_dishes(merchants):
    """为每个商家创建3-10个菜品"""
    print("\n正在创建示例菜品...")
    
    dish_repo = DishRepository()
    all_dishes = []
    
    # 菜品数据模板 - category使用'饭','面','饺子','其他'
    dish_templates = [
        # 饭类
        {"name": "麻辣香锅", "category": "饭", "base_price": 25, "taste": "辣", "spice_level": 4},
        {"name": "黄焖鸡米饭", "category": "饭", "base_price": 22, "taste": "咸", "spice_level": 2},
        {"name": "扬州炒饭", "category": "饭", "base_price": 18, "taste": "咸", "spice_level": 0},
        {"name": "宫保鸡丁", "category": "饭", "base_price": 20, "taste": "酸甜", "spice_level": 2},
        {"name": "红烧肉", "category": "饭", "base_price": 24, "taste": "咸", "spice_level": 0},
        {"name": "鱼香肉丝", "category": "饭", "base_price": 18, "taste": "酸甜", "spice_level": 1},
        {"name": "麻婆豆腐", "category": "饭", "base_price": 12, "taste": "辣", "spice_level": 5},
        
        # 面类
        {"name": "番茄牛肉面", "category": "面", "base_price": 20, "taste": "酸甜", "spice_level": 0},
        {"name": "重庆小面", "category": "面", "base_price": 16, "taste": "辣", "spice_level": 3},
        {"name": "牛肉拉面", "category": "面", "base_price": 15, "taste": "咸", "spice_level": 1},
        {"name": "酸辣粉", "category": "面", "base_price": 12, "taste": "酸甜", "spice_level": 3},
        {"name": "炸酱面", "category": "面", "base_price": 14, "taste": "咸", "spice_level": 0},
        {"name": "担担面", "category": "面", "base_price": 16, "taste": "辣", "spice_level": 4},
        
        # 饺子类
        {"name": "煎饺", "category": "饺子", "base_price": 10, "taste": "咸", "spice_level": 0},
        {"name": "水饺", "category": "饺子", "base_price": 12, "taste": "咸", "spice_level": 0},
        {"name": "蒸饺", "category": "饺子", "base_price": 11, "taste": "咸", "spice_level": 0},
        {"name": "锅贴", "category": "饺子", "base_price": 13, "taste": "咸", "spice_level": 1},
        
        # 其他类
        {"name": "麻辣烫", "category": "其他", "base_price": 18, "taste": "辣", "spice_level": 3},
        {"name": "炸鸡排", "category": "其他", "base_price": 15, "taste": "咸", "spice_level": 1},
        {"name": "春卷", "category": "其他", "base_price": 8, "taste": "咸", "spice_level": 0},
        {"name": "珍珠奶茶", "category": "其他", "base_price": 12, "taste": "淡", "spice_level": 0},
        {"name": "柠檬水", "category": "其他", "base_price": 8, "taste": "酸甜", "spice_level": 0},
        {"name": "豆浆", "category": "其他", "base_price": 5, "taste": "淡", "spice_level": 0},
        {"name": "包子", "category": "其他", "base_price": 3, "taste": "咸", "spice_level": 0},
        {"name": "油条", "category": "其他", "base_price": 2, "taste": "咸", "spice_level": 0},
        {"name": "豆浆油条套餐", "category": "其他", "base_price": 6, "taste": "淡", "spice_level": 0}
    ]
    
    descriptions = {
        "饭": "营养均衡",
        "面": "手工制作",
        "饺子": "皮薄馅大",
        "其他": "特色美食"
    }
    
    # 按category分组菜品模板
    category_dishes = {
        "饭": [d for d in dish_templates if d["category"] == "饭"],
        "面": [d for d in dish_templates if d["category"] == "面"],
        "饺子": [d for d in dish_templates if d["category"] == "饺子"],
        "其他": [d for d in dish_templates if d["category"] == "其他"]
    }
    
    for merchant in merchants:
        # 确保每个商家至少包含所有种类的菜品
        merchant_dishes = []
        
        # 为每个种类至少添加1个菜品
        for category in ["饭", "面", "饺子", "其他"]:
            if category_dishes[category]:
                dish_template = random.choice(category_dishes[category])
                merchant_dishes.append(dish_template)
        
        # 再随机添加一些菜品，总共6-12个菜品
        additional_dishes = random.randint(2, 8)
        all_remaining_dishes = [d for d in dish_templates if d not in merchant_dishes]
        if all_remaining_dishes:
            additional_selected = random.sample(all_remaining_dishes, min(additional_dishes, len(all_remaining_dishes)))
            merchant_dishes.extend(additional_selected)
        
        for template in merchant_dishes:
            try:
                # 在基础价格上浮动±3元
                price = template["base_price"] + random.randint(-3, 3)
                price = max(5, price)  # 最低5元
                
                dish_data = {
                    "merchantId": merchant["id"],
                    "name": template["name"],
                    "description": f"{template['name']}，{descriptions[template['category']]}",
                    "price": price,
                    "category": template["category"],
                    "taste": template["taste"],
                    "spice_level": template["spice_level"],
                    "image_url": "",
                    "is_available": True,
                    "stock_quantity": random.randint(10, 100),
                    "rating": round(random.uniform(3.5, 5.0), 1)
                }
                
                dish = dish_repo.create_dish(dish_data)
                if dish:
                    all_dishes.append(dish)
                    print(f"✓ 为商家 {merchant['storeName']} 创建菜品: {template['name']} ({template['category']}, ¥{price})")
                else:
                    print(f"✗ 创建菜品失败: {template['name']}")
                    
            except Exception as e:
                print(f"✗ 创建菜品 {template['name']} 时出错: {e}")
    
    return all_dishes


def create_traffic_data(merchants):
    """为每个商家创建客流量数据"""
    print("\n正在创建客流量数据...")
    
    merchant_repo = MerchantRepository()
    
    for merchant in merchants:
        try:
            # 生成随机的客流量和等待时间
            count = random.randint(5, 80)  # 5-80人
            waiting_time = random.randint(0, 10)  # 0-10分钟
            
            traffic_data = {
                "merchantId": merchant["id"],
                "count": count,
                "waitingTime": waiting_time,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            traffic_record = merchant_repo.record_traffic(traffic_data)
            if traffic_record:
                print(f"✓ 为商家 {merchant['storeName']} 创建客流量: {count}人, 等待时间: {waiting_time}分钟")
            else:
                print(f"✗ 创建客流量数据失败: {merchant['storeName']}")
                
        except Exception as e:
            print(f"✗ 创建客流量数据时出错: {e}")


def main():
    """主函数"""
    print("开始生成测试数据...")
    
    try:
        # 1. 清空所有表
        clear_all_tables()
        
        # 2. 创建示例用户
        users = create_sample_users()
        
        # 3. 创建示例商家
        merchants = create_sample_merchants()
        
        # 4. 为商家创建菜品
        dishes = create_sample_dishes(merchants)
        
        # 5. 创建客流量数据
        create_traffic_data(merchants)
        
        print(f"\n✅ 测试数据生成完成！")
        print(f"   创建了 {len(users)} 个用户")
        print(f"   创建了 {len(merchants)} 个商家")
        print(f"   创建了 {len(dishes)} 个菜品")
        print(f"\n测试账号信息:")
        print(f"   普通用户: user1 / password123")
        print(f"   商家账号: merchant1 / merchant123")
        
    except Exception as e:
        print(f"❌ 测试数据生成失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
