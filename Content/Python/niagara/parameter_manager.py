"""
Niagara 参数管理器
封装 C++ API 调用，提供 Python 友好的接口
"""

import unreal
from utils.config import Config


class ParameterManager:
    """Niagara 参数管理器（调用 C++ API）"""
    
    def __init__(self, namespace=None):
        """
        初始化参数管理器
        Args:
            namespace: 默认命名空间（User/Engine/System/Emitter）
        """
        self.namespace = namespace or Config.get_default_namespace()
    
    # ==================== 场景组件管理 ====================
    
    @staticmethod
    def get_all_niagara_components():
        """
        获取场景中所有 Niagara 组件
        Returns:
            list[UNiagaraComponent]: Niagara 组件列表
        """
        try:
            components = unreal.ExposeNiagaraVariablesEditorBPLibrary.get_all_niagara_components_in_scene()
            unreal.log(f"🔍 找到 {len(components)} 个 Niagara 组件")
            return components
        except Exception as e:
            unreal.log_error(f"❌ 获取 Niagara 组件失败: {e}")
            return []
    
    @staticmethod
    def get_parameter_names(component):
        """
        获取组件的所有参数名称
        Args:
            component: UNiagaraComponent
        Returns:
            list[str]: 参数名称列表
        """
        try:
            names = unreal.ExposeNiagaraVariablesEditorBPLibrary.get_niagara_variable_names(component)
            return names
        except Exception as e:
            unreal.log_error(f"❌ 获取参数名称失败: {e}")
            return []
    
    # ==================== 参数读取（调用 C++ Get 函数）====================
    
    def get_float(self, component, param_name):
        """读取 Float 参数"""
        try:
            value = unreal.NiagaraVariableHelpers.get_niagara_variable_float(
                component, param_name, self.namespace
            )
            return value
        except Exception as e:
            unreal.log_warning(f"⚠️ 读取 Float 参数 {param_name} 失败: {e}")
            return 0.0
    
    def get_color(self, component, param_name):
        """读取 Color 参数"""
        try:
            color = unreal.NiagaraVariableHelpers.get_niagara_variable_color(
                component, param_name, self.namespace
            )
            return color
        except Exception as e:
            unreal.log_warning(f"⚠️ 读取 Color 参数 {param_name} 失败: {e}")
            return unreal.LinearColor(1, 1, 1, 1)
    
    def get_vector(self, component, param_name):
        """读取 Vector 参数"""
        try:
            vec = unreal.NiagaraVariableHelpers.get_niagara_variable_vec3(
                component, param_name, self.namespace
            )
            return vec
        except Exception as e:
            unreal.log_warning(f"⚠️ 读取 Vector 参数 {param_name} 失败: {e}")
            return unreal.Vector(0, 0, 0)
    
    def get_bool(self, component, param_name):
        """读取 Bool 参数"""
        try:
            value = unreal.NiagaraVariableHelpers.get_niagara_variable_bool(
                component, param_name, self.namespace
            )
            return value
        except Exception as e:
            unreal.log_warning(f"⚠️ 读取 Bool 参数 {param_name} 失败: {e}")
            return False
    
    # ==================== 参数写入（调用 C++ Set 函数）====================
    
    def set_float(self, component, param_name, value):
        """
        设置 Float 参数
        Args:
            component: UNiagaraComponent
            param_name: 参数名称（如 "SpawnRate"）
            value: float 值
        """
        try:
            unreal.NiagaraVariableHelpers.set_niagara_variable_float(
                component, param_name, float(value), self.namespace
            )
            unreal.log(f"✅ 设置 {param_name} = {value}")
            return True
        except Exception as e:
            unreal.log_error(f"❌ 设置 Float 参数 {param_name} 失败: {e}")
            return False
    
    def set_color(self, component, param_name, r, g, b, a=1.0):
        """
        设置 Color 参数
        Args:
            component: UNiagaraComponent
            param_name: 参数名称
            r, g, b, a: 颜色分量（0-1）
        """
        try:
            color = unreal.LinearColor(r, g, b, a)
            unreal.NiagaraVariableHelpers.set_niagara_variable_color(
                component, param_name, color, self.namespace
            )
            unreal.log(f"✅ 设置 {param_name} = RGBA({r}, {g}, {b}, {a})")
            return True
        except Exception as e:
            unreal.log_error(f"❌ 设置 Color 参数 {param_name} 失败: {e}")
            return False
    
    def set_vector(self, component, param_name, x, y, z):
        """
        设置 Vector 参数
        Args:
            component: UNiagaraComponent
            param_name: 参数名称
            x, y, z: 向量分量
        """
        try:
            vec = unreal.Vector(x, y, z)
            unreal.NiagaraVariableHelpers.set_niagara_variable_vec3(
                component, param_name, vec, self.namespace
            )
            unreal.log(f"✅ 设置 {param_name} = ({x}, {y}, {z})")
            return True
        except Exception as e:
            unreal.log_error(f"❌ 设置 Vector 参数 {param_name} 失败: {e}")
            return False
    
    def set_bool(self, component, param_name, value):
        """设置 Bool 参数"""
        try:
            unreal.NiagaraVariableHelpers.set_niagara_variable_bool(
                component, param_name, bool(value), self.namespace
            )
            unreal.log(f"✅ 设置 {param_name} = {value}")
            return True
        except Exception as e:
            unreal.log_error(f"❌ 设置 Bool 参数 {param_name} 失败: {e}")
            return False
    
    # ==================== 批量操作 ====================
    
    def get_all_parameters(self, component):
        """
        获取组件的所有参数及其值
        Returns:
            dict: {参数名: 参数值}
        """
        param_names = self.get_parameter_names(component)
        params = {}
        
        for name in param_names:
            # 尝试不同类型读取（简化版，实际应根据类型判断）
            try:
                # 先尝试 Float（最常用）
                value = self.get_float(component, name)
                params[name] = {"type": "float", "value": value}
            except:
                try:
                    # 尝试 Vector
                    value = self.get_vector(component, name)
                    params[name] = {"type": "vector", "value": value}
                except:
                    # 尝试 Color
                    try:
                        value = self.get_color(component, name)
                        params[name] = {"type": "color", "value": value}
                    except:
                        params[name] = {"type": "unknown", "value": None}
        
        return params
