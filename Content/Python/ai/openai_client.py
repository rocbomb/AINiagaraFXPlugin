"""
OpenAI AI 客户端
负责与 OpenAI API 通信，解析响应并应用到 Niagara 参数
"""

import unreal
import json
from utils.config import Config

# 尝试导入 openai 库
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    unreal.log_warning("⚠️ 未安装 openai 库，请在 UE Python 环境中运行: pip install openai")


class NiagaraAIAssistant:
    """AI 驱动的 Niagara 参数调整助手"""
    
    def __init__(self, parameter_manager):
        """
        初始化 AI 助手
        Args:
            parameter_manager: ParameterManager 实例
        """
        self.param_manager = parameter_manager
        self.api_key = Config.get_api_key()
        self.model = Config.get_model_name()
        self.temperature = Config.get_temperature()
        
        if not OPENAI_AVAILABLE:
            unreal.log_error("❌ OpenAI 库不可用")
            return
        
        if not self.api_key:
            unreal.log_error("❌ 未配置 OpenAI API Key")
            return
        
        # 初始化 OpenAI 客户端
        self.client = openai.OpenAI(api_key=self.api_key)
        unreal.log(f"✅ OpenAI 客户端初始化成功（模型: {self.model}）")
    
    def is_available(self):
        """检查 AI 服务是否可用"""
        return OPENAI_AVAILABLE and self.api_key is not None
    
    def adjust_parameters(self, niagara_component, user_input):
        """
        根据用户自然语言输入调整 Niagara 参数
        Args:
            niagara_component: UNiagaraComponent
            user_input: 用户输入的自然语言（如 "让火焰更大更红"）
        Returns:
            bool: 是否调整成功
        """
        if not self.is_available():
            unreal.log_error("❌ AI 服务不可用")
            return False
        
        try:
            unreal.log(f"🤖 AI 处理中: {user_input}")
            
            # 1. 构建提示词
            prompt = self._build_prompt(niagara_component, user_input)
            
            # 2. 调用 OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                response_format={"type": "json_object"}  # 强制 JSON 输出
            )
            
            # 3. 解析响应
            ai_response = response.choices[0].message.content
            unreal.log(f"📡 AI 响应: {ai_response}")
            
            adjustments = json.loads(ai_response)
            
            # 4. 应用参数调整
            success = self._apply_adjustments(niagara_component, adjustments)
            
            if success:
                unreal.log("✅ AI 参数调整完成!")
                explanation = adjustments.get("explanation", "无说明")
                unreal.log(f"💡 调整说明: {explanation}")
            
            return success
            
        except Exception as e:
            unreal.log_error(f"❌ AI 调整失败: {e}")
            import traceback
            unreal.log_error(traceback.format_exc())
            return False
    
    def _get_system_prompt(self):
        """获取系统提示词"""
        return """你是 Unreal Engine Niagara 粒子系统专家。
你的任务是将用户的自然语言描述转换为 Niagara 参数调整指令。

常见参数说明：
- SpawnRate (Float): 粒子生成速率，值越大粒子越多
- Color (LinearColor): 粒子颜色，RGBA 格式 (0-1)
- Size (Vector): 粒子大小，XYZ 三个方向的缩放
- Velocity (Vector): 粒子速度
- Lifetime (Float): 粒子生命周期（秒）

**输出格式要求（必须是有效的 JSON）**:
{
  "parameters": {
    "参数名1": 数值或对象,
    "参数名2": 数值或对象
  },
  "explanation": "调整说明"
}

**示例**:
用户输入: "让火焰更大更红"
输出:
{
  "parameters": {
    "Color": {"r": 1.0, "g": 0.2, "b": 0.1, "a": 1.0},
    "Size": {"x": 2.0, "y": 2.0, "z": 2.0}
  },
  "explanation": "增加了红色分量，并将粒子大小扩大2倍"
}

**重要规则**:
1. 只输出 JSON，不要额外的文字
2. 参数名称必须存在于当前系统中
3. 数值必须合理（避免极端值）
4. Color 格式为 {"r": 0-1, "g": 0-1, "b": 0-1, "a": 0-1}
5. Vector 格式为 {"x": 数值, "y": 数值, "z": 数值}
"""
    
    def _build_prompt(self, component, user_input):
        """构建完整提示词（包含当前参数上下文）"""
        # 获取当前参数列表
        param_names = self.param_manager.get_parameter_names(component)
        
        prompt = f"""当前 Niagara 系统可用参数：
{', '.join(param_names)}

用户需求：{user_input}

请根据用户需求，输出需要调整的参数（JSON 格式）。
"""
        return prompt
    
    def _apply_adjustments(self, component, adjustments):
        """
        应用 AI 生成的参数调整
        Args:
            component: UNiagaraComponent
            adjustments: AI 返回的 JSON 对象
        Returns:
            bool: 是否全部成功
        """
        parameters = adjustments.get("parameters", {})
        if not parameters:
            unreal.log_warning("⚠️ AI 未返回任何参数调整")
            return False
        
        success_count = 0
        total_count = len(parameters)
        
        for param_name, value in parameters.items():
            # 根据值的类型判断参数类型
            if isinstance(value, dict):
                # 可能是 Color 或 Vector
                if "r" in value and "g" in value and "b" in value:
                    # Color
                    r = value.get("r", 1.0)
                    g = value.get("g", 1.0)
                    b = value.get("b", 1.0)
                    a = value.get("a", 1.0)
                    if self.param_manager.set_color(component, param_name, r, g, b, a):
                        success_count += 1
                
                elif "x" in value and "y" in value and "z" in value:
                    # Vector
                    x = value.get("x", 0.0)
                    y = value.get("y", 0.0)
                    z = value.get("z", 0.0)
                    if self.param_manager.set_vector(component, param_name, x, y, z):
                        success_count += 1
            
            elif isinstance(value, (int, float)):
                # Float
                if self.param_manager.set_float(component, param_name, value):
                    success_count += 1
            
            elif isinstance(value, bool):
                # Bool
                if self.param_manager.set_bool(component, param_name, value):
                    success_count += 1
            
            else:
                unreal.log_warning(f"⚠️ 未知参数类型: {param_name} = {value}")
        
        unreal.log(f"📊 参数调整结果: {success_count}/{total_count} 成功")
        return success_count > 0
