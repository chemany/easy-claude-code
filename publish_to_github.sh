#!/bin/bash

# Easy Claude Code GitHub Publisher
# 自动发布项目到GitHub

set -e

echo "🚀 Easy Claude Code GitHub 发布工具"
echo "======================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否已认证GitHub
echo -e "${BLUE}🔍 检查GitHub认证状态...${NC}"
if ! gh auth status >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  未登录GitHub，请先运行认证：${NC}"
    echo "   gh auth login"
    echo
    echo "认证完成后请重新运行此脚本"
    exit 1
fi

echo -e "${GREEN}✅ GitHub认证已就绪${NC}"

# 获取用户名
USERNAME=$(gh api user --jq .login)
echo -e "${BLUE}👤 GitHub用户名: ${USERNAME}${NC}"

# 检查仓库是否已存在
echo -e "${BLUE}🔍 检查仓库是否存在...${NC}"
if gh repo view "${USERNAME}/easy-claude-code" >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  仓库已存在: https://github.com/${USERNAME}/easy-claude-code${NC}"
    read -p "是否要删除现有仓库并重新创建？(y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}🗑️  删除现有仓库...${NC}"
        gh repo delete "${USERNAME}/easy-claude-code" --confirm
    else
        echo "操作已取消"
        exit 0
    fi
fi

# 创建GitHub仓库
echo -e "${BLUE}📦 创建GitHub仓库...${NC}"
gh repo create easy-claude-code \
    --public \
    --description "🚀 Easily switch between different AI providers for Claude Code with a beautiful GUI. Single-file Linux executable with cross-platform terminal support." \
    --clone=false

# 添加远程仓库
echo -e "${BLUE}🔗 配置远程仓库...${NC}"
if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "https://github.com/${USERNAME}/easy-claude-code.git"
else
    git remote add origin "https://github.com/${USERNAME}/easy-claude-code.git"
fi

# 推送代码
echo -e "${BLUE}⬆️  推送代码到GitHub...${NC}"
git push -u origin main

echo -e "${GREEN}✅ 代码推送成功！${NC}"

# 检查是否有发布文件
if [[ ! -f "releases/easy-claude-code-linux-v1.0.0.tar.gz" ]]; then
    echo -e "${YELLOW}⚠️  未找到发布文件，请先运行构建：${NC}"
    echo "   ./build_linux_binary.sh"
    echo "   ./create_release.sh"
    exit 0
fi

# 创建GitHub Release
echo -e "${BLUE}🎉 创建GitHub Release...${NC}"
gh release create v1.0.0 \
    --title "🚀 Easy Claude Code v1.0.0 - Linux Single-File Edition" \
    --notes "$(cat <<'EOF'
## 🎉 Easy Claude Code v1.0.0 - Initial Release

### ✨ 新功能
- 🖥️ 精美的GUI界面，支持一键切换AI提供商
- 🌐 支持多种Cloudflare Workers代理服务
- 📊 实时API健康状态监控  
- 🖥️ 跨平台终端检测和启动
- 📦 Linux单文件可执行程序（18MB）
- 🔧 无需安装依赖，双击即可运行

### 🔗 支持的API服务
- **cc.yovy.app** - OpenRouter API代理
- **claude.nekro.ai** - 多提供商代理（通义千问、智谱AI、Gemini等）
- **月之暗面** - 直连Claude兼容API
- **Anthropic官方** - 官方Claude API
- **自定义端点** - 任何Claude兼容API

### 🌍 支持的系统
- ✅ Ubuntu 20.04+
- ✅ Debian 11+
- ✅ CentOS 8+
- ✅ Fedora 38+
- ✅ openSUSE Leap 15.5+
- ✅ Arch Linux
- ✅ Linux Mint 20+

### 📋 安装方式
1. 下载发布包并解压
2. 复制 `providers.example.json` 为 `providers.json`
3. 编辑配置文件并填入您的API密钥
4. 运行 `./start.sh` 或双击 `easy-claude-code`

### 🔒 安全特性
- 构建过程确保不包含真实API密钥
- 支持配置文件权限管理
- 智能.gitignore防止密钥泄漏

---

**🎯 Made with ❤️ for the Claude Code community**

如有问题，请查看 [INSTALL.md](./release/INSTALL.md) 获取详细安装说明。
EOF
)" \
    releases/easy-claude-code-linux-v1.0.0.tar.gz \
    releases/easy-claude-code-linux-v1.0.0.zip \
    releases/easy-claude-code-linux-v1.0.0.tar.gz.sha256 \
    releases/easy-claude-code-linux-v1.0.0.zip.sha256

echo -e "${GREEN}🎉 GitHub发布完成！${NC}"
echo
echo -e "${BLUE}📋 仓库信息:${NC}"
echo "🌐 仓库地址: https://github.com/${USERNAME}/easy-claude-code"
echo "📦 Release页面: https://github.com/${USERNAME}/easy-claude-code/releases"
echo "💾 克隆命令: git clone https://github.com/${USERNAME}/easy-claude-code.git"

echo
echo -e "${GREEN}✅ 项目已成功发布到GitHub！${NC}"
echo -e "${YELLOW}💡 用户现在可以：${NC}"
echo "   • 直接下载单文件可执行程序"
echo "   • 克隆仓库自己构建"
echo "   • 提交Issue和PR"
echo "   • Star项目以支持开发"