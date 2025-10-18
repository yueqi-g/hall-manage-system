"""
LLM配置模块
配置使用的大模型和API密钥
"""

import os
from typing import Dict, Any, Optional


class LLMConfig:
    """LLM配置类"""
    
    # 支持的LLM提供商
    PROVIDERS = {
        "openai": {
            "name": "OpenAI",
            "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            "base_url": "https://api.openai.com/v1",
            "api_key_env": "OPENAI_API_KEY"
        },
        "azure": {
            "name": "Azure OpenAI",
            "models": ["gpt-4", "gpt-35-turbo"],
            "base_url": None,  # 需要用户配置
            "api_key_env": "AZURE_OPENAI_API_KEY"
        },
        "deepseek": {
            "name": "DeepSeek",
            "models": ["deepseek-chat", "deepseek-coder"],
            "base_url": "https://api.deepseek.com/v1",
            "api_key_env": "DEEPSEEK_API_KEY"
        },
        "zhipu": {
            "name": "智谱AI",
            "models": ["glm-4", "glm-3-turbo"],
            "base_url": "https://open.bigmodel.cn/api/paas/v4",
            "api_key_env": "ZHIPU_API_KEY"
        },
        "qwen": {
            "name": "通义千问",
            "models": ["qwen-turbo", "qwen-plus", "qwen-max"],
            "base_url": "https://dashscope.aliyuncs.com/api/v1",
            "api_key_env": "DASHSCOPE_API_KEY"
        }
    }
    
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.api_key = self._get_api_key()
        self.base_url = self._get_base_url()
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "2000"))
    
    def _get_api_key(self) -> Optional[str]:
        """获取API密钥"""
        provider_info = self.PROVIDERS.get(self.provider)
        if not provider_info:
            raise ValueError(f"不支持的LLM提供商: {self.provider}")
        
        api_key_env = provider_info["api_key_env"]
        api_key = os.getenv(api_key_env)
        
        if not api_key:
            print(f"警告: 未找到环境变量 {api_key_env}，将使用模拟模式")
            return None
        
        return api_key
    
    def _get_base_url(self) -> Optional[str]:
        """获取基础URL"""
        provider_info = self.PROVIDERS.get(self.provider)
        if not provider_info:
            raise ValueError(f"不支持的LLM提供商: {self.provider}")
        
        # 如果基础URL为None，需要用户配置
        if provider_info["base_url"] is None:
            base_url = os.getenv(f"{self.provider.upper()}_BASE_URL")
            if not base_url:
                raise ValueError(f"请配置 {self.provider.upper()}_BASE_URL 环境变量")
            return base_url
        
        return provider_info["base_url"]
    
    def get_client_config(self) -> Dict[str, Any]:
        """获取客户端配置"""
        if not self.api_key:
            return {"mode": "mock"}
        
        return {
            "provider": self.provider,
            "model": self.model,
            "api_key": self.api_key,
            "base_url": self.base_url,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
    
    def is_available(self) -> bool:
        """检查LLM是否可用"""
        return self.api_key is not None
    
    def get_provider_info(self) -> Dict[str, Any]:
        """获取提供商信息"""
        return self.PROVIDERS.get(self.provider, {})
    
    def validate_config(self) -> bool:
        """验证配置"""
        try:
            if not self.is_available():
                print("警告: LLM配置为模拟模式，将使用本地逻辑")
                return True
            
            provider_info = self.PROVIDERS.get(self.provider)
            if not provider_info:
                print(f"错误: 不支持的LLM提供商: {self.provider}")
                return False
            
            if self.model not in provider_info["models"]:
                print(f"警告: 模型 {self.model} 不在推荐列表中，但将继续使用")
            
            return True
            
        except Exception as e:
            print(f"配置验证失败: {e}")
            return False


# 全局配置实例
llm_config = LLMConfig()


def setup_llm_environment():
    """设置LLM环境"""
    print("=== LLM配置信息 ===")
    print(f"提供商: {llm_config.provider}")
    print(f"模型: {llm_config.model}")
    print(f"可用性: {'是' if llm_config.is_available() else '否 (模拟模式)'}")
    
    if llm_config.validate_config():
        print("配置验证: 通过")
    else:
        print("配置验证: 失败")
    
    print("=" * 20)


if __name__ == "__main__":
    setup_llm_environment()
