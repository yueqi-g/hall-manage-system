"""
DeepSeek模型测试脚本
测试DeepSeek模型的连接和功能
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from ai.orchestrator import ai_orchestrator
from config.llm_config import setup_llm_environment

def test_deepseek_connection():
    """测试DeepSeek连接"""
    print("=== DeepSeek模型测试 ===")
    
    # 设置环境变量（请替换为您的实际API密钥）
    os.environ['LLM_PROVIDER'] = 'deepseek'
    os.environ['LLM_MODEL'] = 'deepseek-chat'
    # os.environ['DEEPSEEK_API_KEY'] = '您的DeepSeek API密钥'
    
    # 检查API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ 未设置DEEPSEEK_API_KEY环境变量")
        print("请设置环境变量：export DEEPSEEK_API_KEY=您的API密钥")
        return False
    
    print(f"✅ 已设置DeepSeek API密钥: {api_key[:10]}...")
    
    # 重新初始化配置
    from config.llm_config import llm_config
    llm_config.__init__()  # 重新初始化以读取新环境变量
    
    # 显示配置信息
    setup_llm_environment()
    
    # 测试连接
    from ai.llm_service import LLMService
    llm_service = LLMService()
    
    if llm_service.is_available():
        print("✅ DeepSeek连接成功！")
        return True
    else:
        print("❌ DeepSeek连接失败")
        return False

def test_deepseek_recommendation():
    """测试DeepSeek推荐功能"""
    print("\n=== DeepSeek推荐功能测试 ===")
    
    # 测试查询
    test_queries = [
        "我想吃辣的面食，价格实惠的",
        "推荐清淡的菜品",
        "今天想吃饺子",
        "有什么高评分的饭推荐吗？"
    ]
    
    for query in test_queries:
        print(f"\n--- 测试查询: '{query}' ---")
        try:
            result = ai_orchestrator.process_query(query)
            print(f"处理模式: {result.get('processing_mode', 'unknown')}")
            print(f"响应类型: {result.get('type', 'unknown')}")
            print(f"菜品数量: {len(result.get('dishes', []))}")
            print(f"推荐内容: {result.get('content', '')}")
            
            if result.get('dishes'):
                print("推荐菜品:")
                for i, dish in enumerate(result.get('dishes', []), 1):
                    print(f"  {i}. {dish.get('name', '未知')} - ¥{dish.get('price', 0)}")
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")

def main():
    """主测试函数"""
    print("开始DeepSeek模型测试...")
    
    # 测试连接
    if not test_deepseek_connection():
        print("\n⚠️ 由于连接失败，将使用模拟模式进行测试")
    
    # 测试推荐功能
    test_deepseek_recommendation()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
