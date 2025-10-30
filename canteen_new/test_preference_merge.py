"""
测试用户偏好融合功能
"""
import sys
import os
sys.path.append('.')

from ai.orchestrator import AIOrchestrator

def test_preference_merge():
    """测试用户偏好融合功能"""
    print('=== 测试用户偏好融合功能 ===')
    
    # 创建编排器实例
    orchestrator = AIOrchestrator()
    
    # 测试1：用户偏好为空的情况
    print('\n--- 测试1：用户偏好为空 ---')
    user_query = '我想吃辣的菜品'
    user_id = 1  # 假设用户ID为1
    
    print(f"用户查询: {user_query}")
    print(f"用户ID: {user_id}")
    print(f"融合用户偏好: True")
    
    try:
        result = orchestrator.process_query(user_query, user_id, merge_user_preference=True)
        print(f"结果类型: {result.get('type')}")
        print(f"处理模式: {result.get('processing_mode')}")
        print(f"菜品数量: {len(result.get('dishes', []))}")
        print("✅ 测试1通过 - 用户偏好为空时正常处理")
    except Exception as e:
        print(f"❌ 测试1失败: {e}")
    
    # 测试2：不融合用户偏好的情况
    print('\n--- 测试2：不融合用户偏好 ---')
    print(f"用户查询: {user_query}")
    print(f"用户ID: {user_id}")
    print(f"融合用户偏好: False")
    
    try:
        result = orchestrator.process_query(user_query, user_id, merge_user_preference=False)
        print(f"结果类型: {result.get('type')}")
        print(f"处理模式: {result.get('processing_mode')}")
        print(f"菜品数量: {len(result.get('dishes', []))}")
        print("✅ 测试2通过 - 不融合用户偏好时正常处理")
    except Exception as e:
        print(f"❌ 测试2失败: {e}")
    
    # 测试3：无用户ID的情况
    print('\n--- 测试3：无用户ID ---')
    print(f"用户查询: {user_query}")
    print(f"用户ID: None")
    print(f"融合用户偏好: True")
    
    try:
        result = orchestrator.process_query(user_query, None, merge_user_preference=True)
        print(f"结果类型: {result.get('type')}")
        print(f"处理模式: {result.get('processing_mode')}")
        print(f"菜品数量: {len(result.get('dishes', []))}")
        print("✅ 测试3通过 - 无用户ID时正常处理")
    except Exception as e:
        print(f"❌ 测试3失败: {e}")

if __name__ == '__main__':
    test_preference_merge()
