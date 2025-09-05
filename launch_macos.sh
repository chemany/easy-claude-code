#!/bin/zsh

# Easy Claude Code macOS Launcher (zsh compatible)
# macOS 启动脚本 - 兼容 zsh 和 bash

# 获取脚本所在目录
SCRIPT_DIR="${0:A:h}"
cd "$SCRIPT_DIR"

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请访问 https://www.python.org/downloads/macos/ 安装 Python 3"
    exit 1
fi

# 检查配置文件
CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/easy-claude-code"
CONFIG_FILE="${CONFIG_DIR}/providers.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "📋 首次运行，正在创建配置文件..."
    mkdir -p "$CONFIG_DIR"
    cp "providers.example.json" "$CONFIG_FILE"
    echo "✅ 配置文件已创建：$CONFIG_FILE"
    echo "🔧 请编辑配置文件并填入您的 API keys"
    echo "   可以使用以下命令编辑："
    echo "   nano \"$CONFIG_FILE\""
    echo ""
    read -p "按回车键继续（或 Ctrl+C 取消）..." -r
fi

# 检查虚拟环境
if [[ -d "venv" ]]; then
    echo "🔍 检测到虚拟环境，正在激活..."
    source venv/bin/activate
elif [[ -d ".venv" ]]; then
    echo "🔍 检测到虚拟环境，正在激活..."
    source .venv/bin/activate
fi

# 检查依赖
echo "🔍 检查 Python 依赖..."
python3 -c "import tkinter, aiohttp" 2>/dev/null || {
    echo "⚠️  正在安装缺失的依赖..."
    pip3 install aiohttp
}

# 启动应用
echo "🚀 启动 Easy Claude Code..."
python3 run.py