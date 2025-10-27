"""
测试AI推荐接口
"""
import sys
import os
import django

# 添加项目路径
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
canteen_path = os.path.join(project_path, 'canteen_new')
sys.path.insert(0, canteen_path)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# 导入AI编排器
from ai.orchestrator import ai_orchestrator

def test_ai_recommend():
    """测试AI推荐功能"""
    print("=== 测试AI推荐功能 ===")
    
    # 测试查询
    test_queries = [
        "我想吃辣的面食，价格实惠的",
        "来点清淡的饭",
        "推荐一些便宜好吃的"
    ]
    
    for query in test_queries:
        print(f"\n测试查询: {query}")
        print("-" * 50)
        
        try:
            result = ai_orchestrator.process_query(query, user_id=None)
            
            print(f"处理模式: {result.get('processing_mode')}")
            print(f"推荐类型: {result.get('type')}")
            print(f"推荐内容: {result.get('content')}")
            print(f"菜品数量: {len(result.get('dishes', []))}")
            
            if result.get('dishes'):
                print("\n推荐菜品:")
                for i, dish in enumerate(result['dishes'][:3], 1):
                    print(f"  {i}. {dish.get('name')} - ¥{dish.get('price')} - {dish.get('taste')} - {dish.get('canteen')}")
            
            print("✅ 测试通过")
            
        except Exception as e:
            print(f"❌ 测试失败: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_ai_recommend()



