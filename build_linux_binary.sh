#!/bin/bash

# Easy Claude Code Linux Binary Builder
# 构建Linux单文件可执行版本

set -e

echo "🚀 开始构建 Easy Claude Code Linux 单文件版本..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否在项目根目录
if [[ ! -f "run.py" ]] || [[ ! -f "gui_switcher_v2.py" ]]; then
    echo -e "${RED}❌ 错误：请在项目根目录运行此脚本${NC}"
    exit 1
fi

echo -e "${BLUE}📋 检查构建环境...${NC}"

# 检查虚拟环境
if [[ ! -d "build_env" ]]; then
    echo -e "${YELLOW}⚠️  build_env 虚拟环境不存在，正在创建...${NC}"
    python3 -m venv build_env
    
    echo -e "${BLUE}📦 安装构建依赖...${NC}"
    source build_env/bin/activate
    pip install --upgrade pip
    pip install pyinstaller aiohttp
else
    echo -e "${GREEN}✅ 找到 build_env 虚拟环境${NC}"
    source build_env/bin/activate
fi

# 确保依赖已安装
echo -e "${BLUE}🔍 验证依赖...${NC}"
python3 -c "import pyinstaller, aiohttp, tkinter; print('✅ 所有依赖已就绪')" || {
    echo -e "${YELLOW}⚠️  缺少依赖，正在安装...${NC}"
    pip install pyinstaller aiohttp
}

# 安全检查 - 确保不包含真实的API密钥
if [[ -f "providers.json" ]]; then
    echo -e "${YELLOW}⚠️  检测到 providers.json 文件${NC}"
    if grep -q "sk-or-v1-" providers.json || grep -q "ak-" providers.json || grep -q "sk-" providers.json; then
        echo -e "${RED}❌ 警告：providers.json 包含真实的API密钥！${NC}"
        echo -e "${RED}   为了安全，请先删除或重命名此文件再构建${NC}"
        exit 1
    fi
fi

# 清理之前的构建
if [[ -d "dist" ]]; then
    echo -e "${YELLOW}🧹 清理之前的构建文件...${NC}"
    rm -rf dist/
fi

if [[ -d "build" ]]; then
    rm -rf build/
fi

if [[ -d "release" ]]; then
    rm -rf release/
fi

# 构建单文件可执行程序
echo -e "${BLUE}🔨 开始构建单文件可执行程序...${NC}"
echo "   这可能需要几分钟时间，请耐心等待..."

pyinstaller easy-claude-code.spec

# 检查构建结果
if [[ -f "dist/easy-claude-code" ]]; then
    echo -e "${GREEN}🎉 构建成功！${NC}"
    
    # 获取文件大小
    size=$(du -h dist/easy-claude-code | cut -f1)
    echo -e "${GREEN}📊 可执行文件大小: ${size}${NC}"
    
    # 设置可执行权限
    chmod +x dist/easy-claude-code
    
    echo -e "${BLUE}📂 构建输出位置:${NC}"
    echo "   $(pwd)/dist/easy-claude-code"
    
    # 创建发布目录
    mkdir -p release
    cp dist/easy-claude-code release/
    cp providers.example.json release/
    cp README.md release/
    cp README_CN.md release/
    cp LICENSE release/
    
    echo -e "${GREEN}📦 发布文件已复制到 release/ 目录${NC}"
    
    echo
    echo -e "${BLUE}🚀 使用说明:${NC}"
    echo "1. 将 release/ 目录中的文件复制到目标Linux系统"
    echo "2. 复制 providers.example.json 为 providers.json 并配置API密钥"
    echo "3. 双击 easy-claude-code 启动GUI，或在终端运行: ./easy-claude-code"
    echo
    echo -e "${GREEN}✅ 构建完成！${NC}"
    
else
    echo -e "${RED}❌ 构建失败！请检查错误信息${NC}"
    exit 1
fi

# 显示构建统计
echo
echo -e "${BLUE}📊 构建统计:${NC}"
echo "构建时间: $(date)"
echo "Python版本: $(python3 --version)"
echo "PyInstaller版本: $(pyinstaller --version)"
echo "文件大小: $size"