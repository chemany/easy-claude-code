#!/bin/bash

# Easy Claude Code - macOS 一键运行脚本
# 
# 使用方法：
# 1. 将整个 easy-claude-code 文件夹复制到你的 Mac
# 2. 在终端运行：./run_macos.sh
# 3. 首次运行会自动安装依赖

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "████████████████████████████████████████████████████████"
echo "█                                                      █"
echo "█            🚀 Easy Claude Code for macOS             █"
echo "█                                                      █"
echo "█                  AI Provider Switcher                █"
echo "█                                                      █"
echo "████████████████████████████████████████████████████████"
echo -e "${NC}"
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}📍 工作目录: $(pwd)${NC}"
echo ""

# 检查 macOS 版本
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ 错误：此脚本只能在 macOS 上运行${NC}"
    exit 1
fi

MACOS_VERSION=$(sw_vers -productVersion)
echo -e "${GREEN}✅ macOS 版本: $MACOS_VERSION${NC}"
echo ""

# 检查 Python 3
echo -e "${BLUE}🔍 检查 Python 3...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✅ Python $PYTHON_VERSION 已安装${NC}"
else
    echo -e "${RED}❌ Python 3 未安装${NC}"
    echo ""
    echo -e "${YELLOW}请安装 Python 3：${NC}"
    echo "1. 访问 https://www.python.org/downloads/macos/"
    echo "2. 或使用 Homebrew: brew install python3"
    echo "3. 安装后重新运行此脚本"
    exit 1
fi

# 检查 Homebrew（可选）
if command -v brew &> /dev/null; then
    echo -e "${GREEN}✅ Homebrew 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  Homebrew 未安装（可选）${NC}"
fi

echo ""

# 检查 tkinter
echo -e "${BLUE}🔍 检查 GUI 组件...${NC}"
if python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${GREEN}✅ tkinter (GUI) 可用${NC}"
else
    echo -e "${RED}❌ tkinter 不可用${NC}"
    echo "这可能是 Python 安装的问题。请确保安装了完整的 Python。"
    exit 1
fi

echo ""

# 创建配置目录和文件
CONFIG_DIR="$HOME/.config/easy-claude-code"
CONFIG_FILE="$CONFIG_DIR/providers.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo -e "${BLUE}📋 首次运行，创建配置文件...${NC}"
    mkdir -p "$CONFIG_DIR"
    
    if [[ -f "providers.example.json" ]]; then
        cp "providers.example.json" "$CONFIG_FILE"
        echo -e "${GREEN}✅ 配置文件已创建: $CONFIG_FILE${NC}"
        echo ""
        echo -e "${YELLOW}🔧 下一步：${NC}"
        echo "请编辑配置文件并填入您的 API keys："
        echo ""
        echo -e "${CYAN}  nano \"$CONFIG_FILE\"${NC}"
        echo ""
        echo "或者使用其他编辑器："
        echo "  - VS Code: code \"$CONFIG_FILE\""
        echo "  - TextEdit: open \"$CONFIG_FILE\""
        echo ""
        echo -e "${YELLOW}重要提示：${NC}"
        echo "- 将 'sk-or-v1-your-openrouter-key-here' 替换为您的真实 OpenRouter API key"
        echo "- 将 'ak-your-nekro-api-key-here' 替换为您的真实 Claude Nekro API key"
        echo "- 保存文件后重新运行此脚本"
        echo ""
        read -p "配置完成后按回车键继续，或 Ctrl+C 退出..." -r
    else
        echo -e "${RED}❌ 错误：找不到 providers.example.json${NC}"
        exit 1
    fi
fi

# 检查配置文件是否还是示例
if grep -q "your-openrouter-key-here" "$CONFIG_FILE" || grep -q "your-nekro-api-key-here" "$CONFIG_FILE"; then
    echo -e "${YELLOW}⚠️  检测到示例 API keys${NC}"
    echo "请编辑配置文件并填入真实的 API keys："
    echo -e "${CYAN}  open \"$CONFIG_FILE\"${NC}"
    echo ""
    read -p "配置完成后按回车键继续..." -r
fi

echo ""

# 检查并安装 aiohttp
echo -e "${BLUE}🔍 检查依赖...${NC}"
if python3 -c "import aiohttp" 2>/dev/null; then
    echo -e "${GREEN}✅ aiohttp 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  正在安装 aiohttp...${NC}"
    pip3 install --user aiohttp
fi

echo ""

# 检查虚拟环境（可选）
if [[ -d "venv" ]]; then
    echo -e "${BLUE}🔍 检测到 venv 虚拟环境，正在激活...${NC}"
    source venv/bin/activate
elif [[ -d ".venv" ]]; then
    echo -e "${BLUE}🔍 检测到 .venv 虚拟环境，正在激活...${NC}"
    source .venv/bin/activate
fi

echo ""
echo -e "${CYAN}🚀 启动 Easy Claude Code...${NC}"
echo ""

# 启动应用
python3 run.py