#!/bin/bash

# Easy Claude Code Release Creator
# 创建可分发的发布包

set -e

VERSION="1.0.0"
RELEASE_NAME="easy-claude-code-linux-v${VERSION}"

echo "🚀 创建 Easy Claude Code Linux 发布包 v${VERSION}..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查是否已构建
if [[ ! -d "release" ]] || [[ ! -f "release/easy-claude-code" ]]; then
    echo -e "${RED}❌ 错误：请先运行 ./build_linux_binary.sh 构建程序${NC}"
    exit 1
fi

echo -e "${BLUE}📋 准备发布文件...${NC}"

# 创建发布目录
mkdir -p "releases/${RELEASE_NAME}"

# 复制核心文件
cp release/easy-claude-code "releases/${RELEASE_NAME}/"
cp release/providers.example.json "releases/${RELEASE_NAME}/"
cp release/README.md "releases/${RELEASE_NAME}/"
cp release/README_CN.md "releases/${RELEASE_NAME}/"
cp release/LICENSE "releases/${RELEASE_NAME}/"
cp release/INSTALL.md "releases/${RELEASE_NAME}/"
cp release/easy-claude-code.desktop "releases/${RELEASE_NAME}/"

# 创建版本信息文件
cat > "releases/${RELEASE_NAME}/VERSION" << EOF
Easy Claude Code - Linux Single File Edition
Version: ${VERSION}
Build Date: $(date)
Platform: Linux x86_64
File Size: $(du -h release/easy-claude-code | cut -f1)

Features:
- Single file executable (no installation required)
- Cross-platform terminal support
- Real-time API health monitoring
- Beautiful GUI interface
- Support for multiple AI providers via Cloudflare Workers

Supported Systems:
- Ubuntu 20.04+
- Debian 11+
- CentOS 8+
- Fedora 38+
- openSUSE Leap 15.5+
- Arch Linux
- Linux Mint 20+

For more information, see README.md or README_CN.md
EOF

# 创建快速启动脚本
cat > "releases/${RELEASE_NAME}/start.sh" << 'EOF'
#!/bin/bash

# Easy Claude Code Quick Start Script

echo "🚀 Easy Claude Code - Linux Edition"
echo "======================================"

# 检查配置文件
if [[ ! -f "providers.json" ]]; then
    echo "⚠️  首次运行：正在创建配置文件..."
    cp providers.example.json providers.json
    echo "✅ 已创建 providers.json，请编辑此文件并填入您的API密钥"
    echo
    echo "📝 支持的API服务："
    echo "   • OpenRouter (cc.yovy.app) - 需要 sk-or-v1- 开头的密钥"
    echo "   • claude.nekro.ai - 需要 ak- 开头的密钥"
    echo "   • 月之暗面 - 需要 sk- 开头的密钥"
    echo "   • Anthropic官方 - 需要 sk-ant- 开头的密钥"
    echo
    read -p "配置完成后按回车键继续..." -r
fi

# 检查执行权限
if [[ ! -x "easy-claude-code" ]]; then
    echo "🔧 设置执行权限..."
    chmod +x easy-claude-code
fi

# 启动程序
echo "🎉 启动 Easy Claude Code..."
./easy-claude-code

EOF

chmod +x "releases/${RELEASE_NAME}/start.sh"

echo -e "${GREEN}📦 创建压缩包...${NC}"

# 创建压缩包
cd releases
tar -czf "${RELEASE_NAME}.tar.gz" "${RELEASE_NAME}/"
zip -r "${RELEASE_NAME}.zip" "${RELEASE_NAME}/"
cd ..

# 计算校验和
cd releases
sha256sum "${RELEASE_NAME}.tar.gz" > "${RELEASE_NAME}.tar.gz.sha256"
sha256sum "${RELEASE_NAME}.zip" > "${RELEASE_NAME}.zip.sha256"
cd ..

echo -e "${GREEN}✅ 发布包创建完成！${NC}"
echo
echo -e "${BLUE}📊 发布统计:${NC}"
echo "版本: v${VERSION}"
echo "构建时间: $(date)"
echo "包含文件:"
ls -la "releases/${RELEASE_NAME}/" | tail -n +2

echo
echo -e "${BLUE}📦 发布文件:${NC}"
echo "• releases/${RELEASE_NAME}.tar.gz (Linux 传统格式)"
echo "• releases/${RELEASE_NAME}.zip (跨平台格式)"
echo "• releases/${RELEASE_NAME}.tar.gz.sha256 (校验和)"
echo "• releases/${RELEASE_NAME}.zip.sha256 (校验和)"

echo
echo -e "${GREEN}🎉 可以上传到 GitHub Releases 或其他分发平台！${NC}"
echo
echo -e "${YELLOW}📋 用户安装说明:${NC}"
echo "1. 下载并解压发布包"
echo "2. 运行 ./start.sh 快速开始"
echo "3. 或者查看 INSTALL.md 获得详细安装说明"