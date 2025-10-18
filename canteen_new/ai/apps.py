"""
AI模块的Django应用配置
"""
from django.apps import AppConfig


class AiConfig(AppConfig):
    """AI模块配置"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai'
    verbose_name = 'AI推荐模块'

    def ready(self):
        """应用启动时初始化LLM服务"""
        # 导入并初始化LLM服务
        from .llm_service import llm_service
        from config.llm_config import setup_llm_environment
        
        print("=== AI模块初始化 ===")
        setup_llm_environment()
        
        # 验证LLM服务状态
        if llm_service.client:
            print(f"✅ LLM服务已初始化: {llm_service.client}")
        else:
            print("⚠️ LLM服务使用模拟模式")
        
        print("=" * 30)
