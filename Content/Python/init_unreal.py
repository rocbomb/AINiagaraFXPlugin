"""
AINiagaraFXPlugin - Python 初始化脚本
在 UE 编辑器启动时自动加载，注册编辑器菜单和工具
"""

import unreal

# 插件信息
PLUGIN_NAME = "AI Niagara FX Plugin"
PLUGIN_VERSION = "1.0.0"

def startup():
    """插件启动时调用"""
    unreal.log(f"🚀 {PLUGIN_NAME} v{PLUGIN_VERSION} 正在加载...")
    
    # 注册编辑器菜单
    register_editor_menu()
    
    unreal.log(f"✅ {PLUGIN_NAME} 加载完成!")


def shutdown():
    """插件关闭时调用"""
    unreal.log(f"👋 {PLUGIN_NAME} 已卸载")


def register_editor_menu():
    """注册编辑器菜单项"""
    try:
        menus = unreal.ToolMenus.get()
        
        # 在主菜单栏的 Tools 下添加菜单项
        main_menu = menus.extend_menu("LevelEditor.MainMenu.Tools")
        
        # 创建菜单条目
        entry = unreal.ToolMenuEntry(
            name="AINiagaraFXTool",
            type=unreal.MultiBlockType.MENU_ENTRY
        )
        entry.set_label(unreal.Text("AI Niagara FX Tool"))
        entry.set_tool_tip(unreal.Text("打开 AI 驱动的 Niagara 特效调整工具"))
        
        # 设置点击回调
        entry.set_string_command(
            unreal.ToolMenuStringCommandType.PYTHON,
            custom_type="",
            string="import ui.main_window; ui.main_window.open_tool_window()"
        )
        
        # 添加到菜单
        main_menu.add_menu_entry("AI Tools", entry)
        
        # 刷新菜单
        menus.refresh_all_widgets()
        
        unreal.log("📋 编辑器菜单注册成功: Tools > AI Niagara FX Tool")
        
    except Exception as e:
        unreal.log_warning(f"⚠️ 菜单注册失败: {e}")


# 自动执行启动函数
if __name__ == "__main__":
    startup()
