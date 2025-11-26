"""
配置管理模块
从 UE ProjectSettings 或环境变量读取配置
"""

import unreal
import os

class Config:
    """配置管理器"""
    
    # 默认配置
    DEFAULT_OPENAI_MODEL = "gpt-4"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_NAMESPACE = "User"
    
    @staticmethod
    def get_api_key():
        """
        获取 OpenAI API Key
        优先级：环境变量 > UE ProjectSettings
        """
        # 1. 尝试从环境变量读取
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            unreal.log("✅ 从环境变量加载 OpenAI API Key")
            return api_key
        
        # 2. 尝试从 UE ProjectSettings 读取
        # TODO: 后续实现 UE 项目设置读取
        # settings = unreal.get_default_object(unreal.AINiagaraSettings)
        # api_key = settings.openai_api_key
        
        # 3. 如果都没有，返回 None
        unreal.log_warning("⚠️ 未找到 OpenAI API Key，请设置环境变量 OPENAI_API_KEY")
        return None
    
    @staticmethod
    def get_model_name():
        """获取 AI 模型名称"""
        return os.getenv("OPENAI_MODEL", Config.DEFAULT_OPENAI_MODEL)
    
    @staticmethod
    def get_temperature():
        """获取 AI 温度参数（创造性程度）"""
        temp = os.getenv("OPENAI_TEMPERATURE", str(Config.DEFAULT_TEMPERATURE))
        return float(temp)
    
    @staticmethod
    def get_default_namespace():
        """获取默认的 Niagara 参数命名空间"""
        return Config.DEFAULT_NAMESPACE


def validate_config():
    """验证配置是否完整"""
    issues = []
    
    api_key = Config.get_api_key()
    if not api_key:
        issues.append("缺少 OpenAI API Key")
    
    if issues:
        msg = "配置验证失败:\n" + "\n".join(f"  - {issue}" for issue in issues)
        unreal.log_error(msg)
        return False
    
    unreal.log("✅ 配置验证通过")
    return True
