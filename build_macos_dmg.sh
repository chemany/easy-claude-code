#!/bin/bash

# Easy Claude Code macOS DMG Builder
# 构建 macOS DMG 安装包

set -e

echo "🚀 开始构建 Easy Claude Code macOS DMG 版本..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 检查是否在 macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo -e "${RED}❌ 错误：此脚本只能在 macOS 上运行${NC}"
    exit 1
fi

# 检查是否在项目根目录
if [[ ! -f "run.py" ]] || [[ ! -f "gui_switcher_v2.py" ]]; then
    echo -e "${RED}❌ 错误：请在项目根目录运行此脚本${NC}"
    exit 1
fi

echo -e "${BLUE}📋 检查构建环境...${NC}"

# 检查 Homebrew
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}⚠️  Homebrew 未安装，请先安装 Homebrew：${NC}"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# 检查 create-dmg
if ! command -v create-dmg &> /dev/null; then
    echo -e "${YELLOW}⚠️  create-dmg 未安装，正在安装...${NC}"
    brew install create-dmg
fi

# 检查 Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 未安装${NC}"
    exit 1
fi

# 检查虚拟环境
if [[ ! -d "macos_build_env" ]]; then
    echo -e "${YELLOW}⚠️  macos_build_env 虚拟环境不存在，正在创建...${NC}"
    python3 -m venv macos_build_env
    
    echo -e "${BLUE}📦 安装构建依赖...${NC}"
    source macos_build_env/bin/activate
    pip install --upgrade pip
    pip install pyinstaller py2app setuptools wheel
else
    echo -e "${GREEN}✅ 找到 macos_build_env 虚拟环境${NC}"
    source macos_build_env/bin/activate
fi

# 确保依赖已安装
echo -e "${BLUE}🔍 验证依赖...${NC}"
python3 -c "import pyinstaller, setuptools, wheel; print('✅ 所有依赖已就绪')" || {
    echo -e "${YELLOW}⚠️  缺少依赖，正在安装...${NC}"
    pip install pyinstaller py2app setuptools wheel
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
echo -e "${YELLOW}🧹 清理之前的构建文件...${NC}"
rm -rf dist/
rm -rf build/
rm -rf release-macos/

# 创建 macOS 应用目录结构
echo -e "${BLUE}📁 创建 macOS 应用目录结构...${NC}"
APP_NAME="Easy Claude Code.app"
APP_DIR="dist/${APP_NAME}"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# 构建 macOS 应用
echo -e "${BLUE}🔨 开始构建 macOS 应用...${NC}"
echo "   这可能需要几分钟时间，请耐心等待..."

# 使用 PyInstaller 构建
pyinstaller --onefile \
    --windowed \
    --name "Easy Claude Code" \
    --distpath "${MACOS_DIR}" \
    --workpath build/macos \
    --hidden-import=tkinter \
    --hidden-import=aiohttp \
    run.py

# 检查构建结果
if [[ ! -f "${MACOS_DIR}/Easy Claude Code" ]]; then
    echo -e "${RED}❌ 构建失败！可执行文件未生成${NC}"
    exit 1
fi

# 创建 Info.plist
echo -e "${BLUE}📝 创建 Info.plist...${NC}"
cat > "${CONTENTS_DIR}/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Easy Claude Code</string>
    <key>CFBundleIdentifier</key>
    <string>com.chemany.easy-claude-code</string>
    <key>CFBundleName</key>
    <string>Easy Claude Code</string>
    <key>CFBundleDisplayName</key>
    <string>Easy Claude Code</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSBackgroundOnly</key>
    <false/>
    <key>LSUIElement</key>
    <false/>
</dict>
</plist>
EOF

# 创建应用图标（如果有的话）
if [[ -f "macos/icon.icns" ]]; then
    cp macos/icon.icns "${RESOURCES_DIR}/"
    plutil -insert CFBundleIconFile -string "icon.icns" "${CONTENTS_DIR}/Info.plist"
fi

# 创建 DMG
echo -e "${BLUE}💿 创建 DMG 安装包...${NC}"

# 创建发布目录
mkdir -p release-macos

# 创建 DMG 源目录
DMG_SOURCE_DIR="dmg_source"
mkdir -p "${DMG_SOURCE_DIR}"

# 复制应用到 DMG 源目录
cp -R "${APP_DIR}" "${DMG_SOURCE_DIR}/"

# 复制附加文件
cp providers.example.json "${DMG_SOURCE_DIR}/"
cp README.md "${DMG_SOURCE_DIR}/"
cp README_CN.md "${DMG_SOURCE_DIR}/"
cp LICENSE "${DMG_SOURCE_DIR}/"

# 创建一个符号链接到应用程序文件夹
ln -s /Applications "${DMG_SOURCE_DIR}/Applications"

# 创建 DMG
DMG_NAME="Easy-Claude-Code-macOS"
DMG_PATH="release-macos/${DMG_NAME}.dmg"

# 删除旧的 DMG
if [[ -f "${DMG_PATH}" ]]; then
    rm "${DMG_PATH}"
fi

# 使用 create-dmg 创建 DMG
create-dmg \
    --volname "Easy Claude Code" \
    --volicon "macos/volume.icns" \
    --window-pos 200 120 \
    --window-size 600 300 \
    --icon-size 100 \
    --icon "Easy Claude Code.app" 175 120 \
    --icon "Applications" 425 120 \
    --hide-extension "Easy Claude Code.app" \
    --app-drop-link 425 120 \
    --add-file "providers.example.json" "${DMG_SOURCE_DIR}/providers.example.json" 175 250 \
    --add-file "README.md" "${DMG_SOURCE_DIR}/README.md" 300 250 \
    --add-file "LICENSE" "${DMG_SOURCE_DIR}/LICENSE" 425 250 \
    "${DMG_PATH}" \
    "${DMG_SOURCE_DIR}"

# 清理临时文件
rm -rf "${DMG_SOURCE_DIR}"

# 检查 DMG 是否创建成功
if [[ -f "${DMG_PATH}" ]]; then
    echo -e "${GREEN}🎉 DMG 创建成功！${NC}"
    
    # 获取文件大小
    size=$(du -h "${DMG_PATH}" | cut -f1)
    echo -e "${GREEN}📊 DMG 文件大小: ${size}${NC}"
    
    echo -e "${CYAN}📂 输出位置:${NC}"
    echo "   ${DMG_PATH}"
    
    echo -e "${BLUE}📋 构建统计:${NC}"
    echo "   构建时间: $(date)"
    echo "   Python版本: $(python3 --version)"
    echo "   macOS版本: $(sw_vers -productVersion)"
    echo "   DMG大小: ${size}"
    
    echo
    echo -e "${CYAN}🚀 使用说明:${NC}"
    echo "1. 下载 ${DMG_NAME}.dmg 到 macOS 系统"
    echo "2. 双击 DMG 文件挂载"
    echo "3. 将 Easy Claude Code.app 拖拽到 Applications 文件夹"
    echo "4. 首次运行时，右键点击应用选择'打开'以绕过Gatekeeper"
    echo "5. 复制 providers.example.json 为 ~/.config/easy-claude-code/providers.json"
    echo "6. 编辑配置文件并填入您的 API keys"
    
else
    echo -e "${RED}❌ DMG 创建失败！${NC}"
    exit 1
fi

echo -e "${GREEN}✅ macOS DMG 构建完成！${NC}"