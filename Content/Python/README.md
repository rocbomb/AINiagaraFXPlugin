# AINiagaraFXPlugin - 快速开始指南

## 📋 概述

这是一个基于 **混合架构（C++ API + Python UI/AI）** 的 UE5 编辑器工具，可以通过自然语言指令调整 Niagara 粒子特效参数。

### 架构说明
- **C++ 层**: 提供高性能的 Niagara 参数读写 API
- **Python 层**: UI 界面和 AI 集成（OpenAI）

---

## 🚀 快速开始

### 1. 环境要求

- ✅ Unreal Engine 5.5
- ✅ Python 3.x（UE 内置）
- ✅ OpenAI API Key（用于 AI 功能）

### 2. 安装插件

插件已经配置好，直接使用即可。

**检查插件是否加载**：
1. 打开 UE 编辑器
2. 编辑 > 插件 > 搜索 "AINiagaraFXPlugin"
3. 确保插件已启用

### 3. 安装 Python 依赖

在 UE 编辑器的 Python 控制台中运行：

```python
# 方法1: 使用 UE 的 Python
import subprocess
subprocess.run(["pip", "install", "openai"])

# 方法2: 在系统 PowerShell 中
# 找到 UE 的 Python.exe，通常在:
# C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\ThirdParty\Python3\Win64\python.exe
# 然后运行:
# python.exe -m pip install openai
```

### 4. 配置 API Key

**Windows PowerShell**:
```powershell
# 临时设置（当前会话）
$env:OPENAI_API_KEY = "your_api_key_here"

# 永久设置（系统环境变量）
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your_api_key_here", "User")
```

**验证配置**:
```python
import os
print(os.getenv("OPENAI_API_KEY"))  # 应该输出你的 Key
```

---

## 💡 使用方法

### 方法1: 通过编辑器菜单（推荐）

1. 在场景中添加 Niagara 系统（如果还没有）
2. 点击菜单: **Tools > AI Niagara FX Tool**
3. 对话框会显示场景中的 Niagara 组件列表
4. 查看输出日志，使用 Python 命令调整参数

### 方法2: Python 控制台直接调用

**打开 Python 控制台**:
- UE 编辑器 > Tools > Python > Open Python Console

**示例命令**:

```python
# 1. 导入模块
import ui.main_window

# 2. 打开工具窗口（查看可用组件）
ui.main_window.open_tool_window()

# 3. 调整参数（组件索引, 自然语言描述）
ui.main_window.select_component_and_adjust(0, "让火焰更大更红")

# 4. 更多示例
ui.main_window.select_component_and_adjust(0, "减慢粒子速度")
ui.main_window.select_component_and_adjust(0, "增加粒子数量")
ui.main_window.select_component_and_adjust(0, "改成蓝色")
```

### 方法3: 快速测试

```python
import ui.main_window
ui.main_window.quick_test()  # 测试是否正常工作
```

---

## 📚 API 使用示例

### Python 直接调用 C++ API

```python
import unreal
from niagara.parameter_manager import ParameterManager

# 创建参数管理器
pm = ParameterManager()

# 获取场景中的所有 Niagara 组件
components = pm.get_all_niagara_components()
comp = components[0]

# 读取参数
spawn_rate = pm.get_float(comp, "SpawnRate")
color = pm.get_color(comp, "Color")

# 设置参数
pm.set_float(comp, "SpawnRate", 500.0)
pm.set_color(comp, "Color", 1.0, 0.5, 0.2, 1.0)  # 橙色
pm.set_vector(comp, "Size", 2.0, 2.0, 2.0)  # 放大2倍
```

### 使用 AI 助手

```python
from niagara.parameter_manager import ParameterManager
from ai.openai_client import NiagaraAIAssistant

pm = ParameterManager()
ai = NiagaraAIAssistant(pm)

components = pm.get_all_niagara_components()
comp = components[0]

# 通过自然语言调整
ai.adjust_parameters(comp, "让粒子更密集")
ai.adjust_parameters(comp, "改成绿色的魔法效果")
```

---

## 🔧 故障排查

### 问题1: "未安装 openai 库"

**解决方案**:
```python
import subprocess
subprocess.run(["pip", "install", "openai"])
```

### 问题2: "未找到 OpenAI API Key"

**解决方案**:
1. 确认环境变量已设置
2. **重启 UE 编辑器**（重要！）
3. 在 Python 控制台验证: `import os; print(os.getenv("OPENAI_API_KEY"))`

### 问题3: "未找到 Niagara 组件"

**解决方案**:
1. 在场景中添加 Niagara Actor 或组件
2. 确保组件已激活
3. 运行 `ui.main_window.quick_test()` 检查

### 问题4: C++ API 调用失败

**解决方案**:
1. 检查插件是否正确加载: 编辑 > 插件
2. 重新编译 C++ 代码（如果修改过）
3. 查看输出日志中的详细错误信息

---

## 📂 文件结构

```
AINiagaraFXPlugin/
├── Content/Python/              # Python 脚本
│   ├── init_unreal.py          # 插件初始化
│   ├── ui/
│   │   └── main_window.py      # 主窗口
│   ├── ai/
│   │   └── openai_client.py    # AI 客户端
│   ├── niagara/
│   │   └── parameter_manager.py # 参数管理器
│   └── utils/
│       └── config.py            # 配置管理
│
├── Source/                      # C++ 源代码
│   ├── AINiagaraFXPluginEditor/
│   │   ├── Public/
│   │   │   ├── NiagaraVariableHelpers.h
│   │   │   └── ExposeNiagaraVariablesEditorBPLibrary.h
│   │   └── Private/
│   │       ├── NiagaraVariableHelpers.cpp
│   │       └── ExposeNiagaraVariablesEditorBPLibrary.cpp
│   └── AINiagaraFXPlugin/       # Runtime 模块（已改为 Editor）
│
└── AINiagaraFXPlugin.uplugin    # 插件配置
```

---

## 🎯 下一步

1. ✅ 尝试基础功能（参数读写）
2. ✅ 测试 AI 调整功能
3. 📝 根据需要扩展功能：
   - 添加更多参数类型支持
   - 开发完整的 UI 面板（使用 EditorUtilityWidget）
   - 添加预设系统
   - 历史记录和撤销功能

---

## 🤝 反馈与支持

- 🐛 报告问题: 查看输出日志
- 💡 功能建议: 欢迎提出
- 📖 文档: 查看 `开发计划书.md`

---

**Happy Coding! 🎉**
