"""
测试新的AI模块架构
验证编排器、关键词提取器、LLM服务等模块的协同工作
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ai.orchestrator import ai_orchestrator
from ai.keyword_extractor import keyword_extractor
from ai.llm_service import llm_service
from ai.context_service import ContextService


def test_keyword_extractor():
    """测试关键词提取器"""
    print("=== 测试关键词提取器 ===")
    
    test_queries = [
        "我想吃辣的面条",
        "推荐便宜的饭",
        "想吃酸甜口味的菜",
        "今天想吃饺子",
        "有什么清淡的菜品推荐吗？"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        params = keyword_extractor.extract(query)
        print(f"提取参数: {params}")
        
        summary = keyword_extractor.get_extraction_summary(query)
        print(f"提取摘要: {summary}")


def test_context_service():
    """测试情景数据服务"""
    print("\n=== 测试情景数据服务 ===")
    
    context_service = ContextService()
    
    # 测试获取所有情景数据
    context_data = context_service.get_all_context_data()
    print(f"情景数据: {context_data}")


def test_llm_service():
    """测试LLM服务"""
    print("\n=== 测试LLM服务 ===")
    
    print(f"LLM可用性: {llm_service.is_available()}")
    print(f"LLM模式: {'模拟模式' if llm_service.client is None else '真实模式'}")


def test_orchestrator():
    """测试编排器完整流程"""
    print("\n=== 测试编排器完整流程 ===")
    
    test_queries = [
        "我想吃辣的面食，价格实惠的",
        "推荐清淡的菜品",
        "想吃饺子",
        "有什么高评分的饭推荐吗？"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"测试查询: {query}")
        print('='*50)
        
        result = ai_orchestrator.process_query(query)
        
        print(f"\n处理模式: {result.get('processing_mode')}")
        print(f"响应类型: {result.get('type')}")
        print(f"菜品数量: {len(result.get('dishes', []))}")
        
        print(f"\n推荐内容:")
        print(result.get('content', '无内容'))
        
        if result.get('dishes'):
            print(f"\n菜品详情:")
            for i, dish in enumerate(result.get('dishes', []), 1):
                print(f"  {i}. {dish.get('name')} - ¥{dish.get('price')} - {dish.get('category')} - {dish.get('taste')}")


def main():
    """主测试函数"""
    print("开始测试新的AI模块架构...")
    
    # 测试各模块
    test_keyword_extractor()
    test_context_service()
    test_llm_service()
    test_orchestrator()
    
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    main()
