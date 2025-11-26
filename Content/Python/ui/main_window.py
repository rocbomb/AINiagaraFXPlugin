"""
AI Niagara FX Tool - 主窗口
提供可视化界面用于选择 Niagara 组件并通过 AI 调整参数
"""

import unreal
import sys
import os

# 添加 Python 脚本路径到 sys.path
plugin_python_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if plugin_python_path not in sys.path:
    sys.path.insert(0, plugin_python_path)

from niagara.parameter_manager import ParameterManager
from ai.openai_client import NiagaraAIAssistant


class AINiagaraToolWindow:
    """AI Niagara 工具窗口（简化版，使用对话框）"""
    
    def __init__(self):
        self.param_manager = ParameterManager()
        self.ai_assistant = NiagaraAIAssistant(self.param_manager)
        self.selected_component = None
        self.components = []
    
    def show(self):
        """显示工具窗口"""
        unreal.log("🪟 打开 AI Niagara FX 工具")
        
        # 获取场景中的 Niagara 组件
        self.components = self.param_manager.get_all_niagara_components()
        
        if not self.components:
            self._show_message("未找到 Niagara 组件", 
                             "请在场景中添加 Niagara 组件后再使用本工具。")
            return
        
        # 显示组件选择对话框
        self._show_component_selector()
    
    def _show_component_selector(self):
        """显示组件选择器"""
        component_names = []
        for i, comp in enumerate(self.components):
            actor = comp.get_owner()
            actor_name = actor.get_name() if actor else "Unknown"
            asset = comp.get_asset()
            asset_name = asset.get_name() if asset else "No Asset"
            component_names.append(f"{i}. {actor_name} - {asset_name}")
        
        message = "选择要调整的 Niagara 组件:\n\n" + "\n".join(component_names)
        message += "\n\n请在输出日志中输入组件编号（0-{})".format(len(self.components) - 1)
        
        self._show_message("选择 Niagara 组件", message)
        unreal.log("=" * 60)
        unreal.log("📋 场景中的 Niagara 组件:")
        for name in component_names:
            unreal.log(f"  {name}")
        unreal.log("=" * 60)
        unreal.log("💡 使用方法:")
        unreal.log("  1. 在 Python 控制台中运行:")
        unreal.log("     import ui.main_window")
        unreal.log("     ui.main_window.select_component_and_adjust(组件编号, '调整需求')")
        unreal.log("  2. 示例:")
        unreal.log("     ui.main_window.select_component_and_adjust(0, '让火焰更大更红')")
        unreal.log("=" * 60)
    
    def _show_message(self, title, message):
        """显示消息对话框"""
        text = unreal.Text(message)
        unreal.EditorDialog.show_message(
            unreal.Text(title),
            text,
            unreal.AppMsgType.OK
        )
    
    def adjust_component(self, component_index, user_input):
        """
        调整指定组件
        Args:
            component_index: 组件索引
            user_input: 用户输入的调整需求
        """
        if component_index < 0 or component_index >= len(self.components):
            unreal.log_error(f"❌ 无效的组件索引: {component_index}")
            return False
        
        self.selected_component = self.components[component_index]
        actor = self.selected_component.get_owner()
        actor_name = actor.get_name() if actor else "Unknown"
        
        unreal.log(f"🎯 选中组件: {actor_name}")
        unreal.log(f"💬 用户输入: {user_input}")
        
        # 检查 AI 服务是否可用
        if not self.ai_assistant.is_available():
            self._show_message("AI 服务不可用", 
                             "请配置 OpenAI API Key 后重试。\n\n"
                             "设置方法:\n"
                             "1. Windows: set OPENAI_API_KEY=your_key\n"
                             "2. 重启 UE 编辑器")
            return False
        
        # 调用 AI 调整参数
        success = self.ai_assistant.adjust_parameters(
            self.selected_component, 
            user_input
        )
        
        if success:
            self._show_message("调整成功", f"AI 已完成参数调整!\n\n输入: {user_input}")
        else:
            self._show_message("调整失败", "AI 调整失败，请查看输出日志获取详细信息。")
        
        return success


# ==================== 全局辅助函数 ====================

_tool_window = None

def open_tool_window():
    """打开工具窗口（从菜单调用）"""
    global _tool_window
    _tool_window = AINiagaraToolWindow()
    _tool_window.show()


def select_component_and_adjust(component_index, user_input):
    """
    选择组件并调整（简化版 API）
    
    使用示例:
        import ui.main_window
        ui.main_window.select_component_and_adjust(0, "让火焰更大更红")
    
    Args:
        component_index: 组件索引（从 0 开始）
        user_input: 自然语言描述的调整需求
    """
    global _tool_window
    
    # 如果窗口未创建，先创建
    if _tool_window is None:
        _tool_window = AINiagaraToolWindow()
        _tool_window.components = _tool_window.param_manager.get_all_niagara_components()
    
    # 执行调整
    _tool_window.adjust_component(component_index, user_input)


def quick_test():
    """快速测试函数"""
    unreal.log("🧪 开始快速测试...")
    
    # 1. 测试参数管理器
    param_manager = ParameterManager()
    components = param_manager.get_all_niagara_components()
    
    if not components:
        unreal.log_error("❌ 场景中没有 Niagara 组件，无法测试")
        return
    
    comp = components[0]
    unreal.log(f"✅ 找到组件: {comp.get_owner().get_name()}")
    
    # 2. 测试参数读取
    params = param_manager.get_parameter_names(comp)
    unreal.log(f"✅ 参数列表: {params}")
    
    # 3. 测试 AI（如果可用）
    ai = NiagaraAIAssistant(param_manager)
    if ai.is_available():
        unreal.log("✅ AI 服务可用")
    else:
        unreal.log("⚠️ AI 服务不可用（需要配置 API Key）")
    
    unreal.log("✅ 快速测试完成!")
