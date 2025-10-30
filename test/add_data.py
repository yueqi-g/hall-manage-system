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
    """按指定食堂分配创建示例商家（不随机分配）。"""
    print("\n正在创建示例商家...")
    
    user_repo = UserRepository()
    merchant_repo = MerchantRepository()
    merchants = []
    
    # 固定食堂-店铺映射
    canteen_map = {
        "一食堂": ["川菜窗口", "淮扬快餐", "印度飞饼"],
        "二食堂": ["陈香贵面馆", "吉祥馄饨", "绿园餐厅"],
        "三食堂": ["西式快餐", "麻辣烫"],
        "四食堂": ["粤式烧腊", "韩式料理"],
    }

    # 展平为列表并带上食堂
    merchant_data = []
    username_idx = 1
    for hall, stores in canteen_map.items():
        for store in stores:
            merchant_data.append({
                "username": f"merchant{username_idx}",
                "store_name": store,
                "email": f"merchant{username_idx}@example.com",
                "canteen": hall,
            })
            username_idx += 1

    for data in merchant_data:
        
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
                "canteen": data["canteen"],
                "location": f"{data['canteen']} {random.randint(1, 20)}号窗口",
                "contact_info": f"电话: 138-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
                "description": f"专业制作{data['store_name']}特色美食，欢迎品尝！"
            }
            
            merchant = merchant_repo.create_merchant(merchant_create_data)
            if merchant:
                merchants.append(merchant)
                print(f"✓ 创建商家: {data['store_name']} ({data['canteen']})")
            else:
                print(f"✗ 创建商家记录失败: {data['store_name']}")
                
        except Exception as e:
            print(f"✗ 创建商家 {data['store_name']} 时出错: {e}")
    
    return merchants


def create_sample_dishes(merchants):
    """基于模板为每个商家创建菜品（使用填写的价格与商家，不做随机价格）。"""
    print("\n正在创建示例菜品...")
    
    dish_repo = DishRepository()
    all_dishes = []
    
    # 菜品数据模板（按商家分组），直接使用填写的价格
    dish_templates = [
        {"merchant": "川菜窗口", "dishes": [
            {"name": "麻婆豆腐", "description": "经典川菜，麻辣鲜香", "price": 18.0, "category": "其他", "taste": "辣", "spice_level": 4},
            {"name": "水煮肉片", "description": "肉质鲜嫩，麻辣过瘾", "price": 20.0, "category": "其他", "taste": "辣", "spice_level": 5},
            {"name": "宫保鸡丁", "description": "酸甜微辣，鸡肉嫩滑", "price": 16.0, "category": "其他", "taste": "酸甜", "spice_level": 3},
            {"name": "回锅肉", "description": "肥而不腻，香气扑鼻", "price": 20.0, "category": "其他", "taste": "辣", "spice_level": 3},
            {"name": "四川麻辣鹅", "description": "肉质鲜嫩，麻辣爽口", "price": 22.0, "category": "其他", "taste": "辣", "spice_level": 4}
        ]},
        {"merchant": "陈香贵面馆", "dishes": [
            {"name": "兰州牛肉拉面", "description": "汤清肉烂，面条筋道", "price": 16.0, "category": "面", "taste": "咸", "spice_level": 0},
            {"name": "酸菜牛肉面", "description": "酸爽开胃，牛肉鲜嫩", "price": 18.0, "category": "面", "taste": "咸", "spice_level": 0},
            {"name": "油泼面", "description": "香辣过瘾，面条宽厚", "price": 16.0, "category": "面", "taste": "辣", "spice_level": 2},
            {"name": "臊子面", "description": "配料丰富，味道浓郁", "price": 17.0, "category": "面", "taste": "咸", "spice_level": 0},
            {"name": "凉拌牛肉", "description": "肉质鲜嫩，调味恰到好处", "price": 10.0, "category": "其他", "taste": "咸", "spice_level": 0}
        ]},
        {"merchant": "粤式烧腊", "dishes": [
            {"name": "烧鸭饭", "description": "皮脆肉嫩，香气四溢", "price": 15.0, "category": "饭", "taste": "咸", "spice_level": 0},
            {"name": "叉烧", "description": "甜咸适中，肉质鲜嫩", "price": 12.0, "category": "其他", "taste": "甜", "spice_level": 0},
            {"name": "白切鸡饭", "description": "鸡肉鲜嫩，原汁原味", "price": 18.0, "category": "饭", "taste": "咸", "spice_level": 0},
            {"name": "烧肉", "description": "皮脆肉香，肥瘦相间", "price": 18.0, "category": "其他", "taste": "咸", "spice_level": 0},
            {"name": "豉油鸡", "description": "色泽红亮，豉油香浓", "price": 16.0, "category": "饭", "taste": "咸", "spice_level": 0}
        ]},
        {"merchant": "吉祥馄饨", "dishes": [
            {"name": "鲜肉饺子", "description": "皮薄馅大，汤汁鲜美", "price": 12.0, "category": "饺子", "taste": "淡", "spice_level": 0},
            {"name": "虾仁饺子", "description": "虾仁饱满，口感Q弹", "price": 18.0, "category": "饺子", "taste": "淡", "spice_level": 0},
            {"name": "荠菜饺子", "description": "野菜清香，营养健康", "price": 14.0, "category": "饺子", "taste": "淡", "spice_level": 0},
            {"name": "红油馄饨", "description": "香辣开胃，馄饨鲜美", "price": 15.0, "category": "饺子", "taste": "辣", "spice_level": 2},
            {"name": "小馄饨", "description": "皮薄馅多，汤汁丰富", "price": 16.0, "category": "饺子", "taste": "淡", "spice_level": 0}
        ]},
        {"merchant": "绿园餐厅", "dishes": [
            {"name": "番茄炒蛋", "description": "家常美味，酸甜可口", "price": 4.0, "category": "其他", "taste": "酸甜", "spice_level": 0},
            {"name": "青椒肉丝", "description": "肉丝嫩滑，青椒爽脆", "price": 6.0, "category": "其他", "taste": "咸", "spice_level": 1},
            {"name": "麻婆豆腐", "description": "麻辣鲜香，下饭佳品", "price": 5.0, "category": "其他", "taste": "辣", "spice_level": 4},
            {"name": "酸辣土豆丝", "description": "酸辣爽口，开胃小菜", "price": 4.0, "category": "其他", "taste": "辣", "spice_level": 2},
            {"name": "紫菜蛋花汤", "description": "清淡鲜美，营养丰富", "price": 1.0, "category": "其他", "taste": "淡", "spice_level": 0}
        ]},
        {"merchant": "淮扬快餐", "dishes": [
            {"name": "扬州炒饭", "description": "米饭粒粒分明，配料丰富", "price": 6.0, "category": "饭", "taste": "咸", "spice_level": 0},
            {"name": "狮子头", "description": "肉质鲜嫩，汤汁浓郁", "price": 8.0, "category": "其他", "taste": "咸", "spice_level": 0},
            {"name": "大煮干丝", "description": "刀工精细，汤鲜味美", "price": 3.0, "category": "其他", "taste": "咸", "spice_level": 0},
            {"name": "糖醋排骨", "description": "酸甜适中，排骨酥烂", "price": 8.0, "category": "其他", "taste": "酸甜", "spice_level": 0},
            {"name": "清炒时蔬", "description": "时令蔬菜，清淡健康", "price": 2.0, "category": "其他", "taste": "淡", "spice_level": 0}
        ]},
        {"merchant": "麻辣烫", "dishes": [
            {"name": "经典麻辣烫", "description": "多种食材，麻辣鲜香", "price": 20.0, "category": "其他", "taste": "辣", "spice_level": 4},
            {"name": "番茄麻辣烫", "description": "酸甜开胃，适合不吃辣", "price": 18.0, "category": "其他", "taste": "酸甜", "spice_level": 0},
            {"name": "骨汤麻辣烫", "description": "汤底浓郁，营养丰富", "price": 18.0, "category": "其他", "taste": "咸", "spice_level": 0},
            {"name": "酸辣粉", "description": "酸辣爽口，粉丝筋道", "price": 15.0, "category": "其他", "taste": "辣", "spice_level": 3},
            {"name": "麻辣拌", "description": "干拌做法，味道更浓", "price": 19.0, "category": "其他", "taste": "辣", "spice_level": 4}
        ]},
        {"merchant": "韩式料理", "dishes": [
            {"name": "石锅拌饭", "description": "配料丰富，锅巴香脆", "price": 25.0, "category": "主食", "taste": "咸甜", "spice_level": 2},
            {"name": "部队火锅", "description": "多种食材，味道浓郁", "price": 48.0, "category": "火锅", "taste": "咸辣", "spice_level": 3},
            {"name": "炒年糕", "description": "年糕软糯，甜辣适中", "price": 18.0, "category": "小吃", "taste": "甜辣", "spice_level": 2},
            {"name": "大酱汤", "description": "传统韩式汤品，营养丰富", "price": 20.0, "category": "汤类", "taste": "咸鲜", "spice_level": 1},
            {"name": "泡菜煎饼", "description": "外酥里嫩，泡菜风味", "price": 16.0, "category": "小吃", "taste": "酸辣", "spice_level": 2}
        ]},
        {"merchant": "印度飞饼", "dishes": [
            {"name": "香蕉飞饼", "description": "香甜可口，外酥里嫩", "price": 15.0, "category": "饭", "taste": "酸甜", "spice_level": 0},
            {"name": "鸡蛋飞饼", "description": "蛋香浓郁，营养丰富", "price": 12.0, "category": "饭", "taste": "咸", "spice_level": 0},
            {"name": "咖喱鸡肉飞饼", "description": "咖喱风味，鸡肉鲜嫩", "price": 18.0, "category": "饭", "taste": "咸", "spice_level": 1},
            {"name": "黄油飞饼", "description": "黄油香气，简单美味", "price": 10.0, "category": "饭", "taste": "咸", "spice_level": 0},
            {"name": "印度咖喱鸡", "description": "正宗印度风味，香浓可口", "price": 18.0, "category": "其他", "taste": "咸", "spice_level": 1}
        ]},
        {"merchant": "西式快餐", "dishes": [
            {"name": "经典汉堡", "description": "牛肉饼厚实，配料丰富", "price": 20.0, "category": "其他", "taste": "咸", "spice_level": 0},
            {"name": "炸鸡套餐", "description": "外酥里嫩，配薯条可乐", "price": 25.0, "category": "其他", "taste": "咸", "spice_level": 0},
            {"name": "意大利面", "description": "番茄肉酱，面条筋道", "price": 20.0, "category": "面", "taste": "酸甜", "spice_level": 0},
            {"name": "蔬菜沙拉", "description": "新鲜蔬菜，健康轻食", "price": 15.0, "category": "其他", "taste": "淡", "spice_level": 0},
            {"name": "薯条", "description": "金黄酥脆，外酥内软", "price": 12.0, "category": "其他", "taste": "咸", "spice_level": 0}
        ]}
    ]

    # 建立商家名称到模板的映射
    merchant_name_to_templates = {item["merchant"]: item["dishes"] for item in dish_templates}
    
    for merchant in merchants:
        store_name = merchant.get("storeName") or merchant.get("store_name")
        templates = merchant_name_to_templates.get(store_name, [])
        if not templates:
            # 若没有匹配模板则跳过
            print(f"- 跳过商家（无模板）: {store_name}")
            continue

        for tpl in templates:
            try:
                dish_data = {
                    "merchantId": merchant["id"],
                    "name": tpl["name"],
                    "description": tpl.get("description", ""),
                    "price": float(tpl["price"]),
                    "category": tpl.get("category", "其他"),
                    "taste": tpl.get("taste", ""),
                    "spice_level": int(tpl.get("spice_level", 0)),
                    "image_url": "",
                    "is_available": True,
                    "stock_quantity": 50,
                    "rating": 4.5,
                }
                
                dish = dish_repo.create_dish(dish_data)
                if dish:
                    all_dishes.append(dish)
                    print(f"✓ 为商家 {store_name} 创建菜品: {tpl['name']} ({tpl.get('category','其他')}, ¥{tpl['price']})")
                else:
                    print(f"✗ 创建菜品失败: {tpl['name']}")
            except Exception as e:
                print(f"✗ 创建菜品 {tpl.get('name')} 时出错: {e}")
    
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
