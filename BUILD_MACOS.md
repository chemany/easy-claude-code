# macOS 构建说明

## 在 macOS 上构建 DMG 安装包

### 前置要求

1. **macOS 系统**（10.14 或更高版本）
2. **Xcode 命令行工具**
   ```bash
   xcode-select --install
   ```
3. **Homebrew**（包管理器）
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

### 构建步骤

1. **克隆或下载项目**
   ```bash
   git clone https://github.com/chemany/easy-claude-code.git
   cd easy-claude-code
   ```

2. **运行构建脚本**
   ```bash
   ./build_macos_dmg.sh
   ```

   脚本会自动：
   - 检查并安装依赖
   - 创建虚拟环境
   - 构建 macOS 应用
   - 打包为 DMG 文件

3. **查看输出**
   构建完成后，DMG 文件位于：
   ```
   release-macos/Easy-Claude-Code-macOS.dmg
   ```

### 手动构建（可选）

如果你想手动控制构建过程：

1. **设置环境**
   ```bash
   python3 -m venv macos_build_env
   source macos_build_env/bin/activate
   pip install pyinstaller create-dmg
   ```

2. **构建应用**
   ```bash
   pyinstaller --onefile --windowed --name "Easy Claude Code" run.py
   ```

3. **创建 DMG**
   ```bash
   # 创建 DMG 源目录
   mkdir -p dmg_source
   cp -R "dist/Easy Claude Code.app" dmg_source/
   cp providers.example.json dmg_source/
   
   # 创建 DMG
   create-dmg --volname "Easy Claude Code" \
     --window-pos 200 120 \
     --window-size 600 300 \
     --icon-size 100 \
     --icon "Easy Claude Code.app" 175 120 \
     --icon "Applications" 425 120 \
     release-macos/Easy-Claude-Code-macOS.dmg \
     dmg_source
   ```

### zsh 兼容性说明

本项目的 macOS 版本完全兼容 zsh shell：

1. **启动脚本**：`launch_macos.sh` 使用 zsh 语法（`${0:A:h}`）
2. **环境变量**：支持 `${XDG_CONFIG_HOME}` 等标准环境变量
3. **路径处理**：使用 macOS 原生路径格式

### 配置文件位置

在 macOS 上，配置文件位于：
```
~/.config/easy-claude-code/providers.json
```

遵循 XDG Base Directory 规范。

### Gatekeeper 和公证

为了让应用能够正常运行，用户可能需要：

1. **首次运行时右键点击应用，选择"打开"**
2. 或者在系统设置中允许来自未知开发者的应用

如果需要分发到 Mac App Store，需要进行苹果公证（需要 Apple Developer 账户）。

### 故障排除

1. **构建失败**
   - 确保已安装 Xcode 命令行工具
   - 检查 Python 版本（需要 3.8+）
   - 确保有足够的磁盘空间

2. **应用无法启动**
   - 检查 Gatekeeper 设置
   - 确认 API keys 配置正确
   - 查看控制台日志

3. **依赖问题**
   ```bash
   # 重新安装依赖
   pip install --force-reinstall pyinstaller
   ```

### 更新 DMG

当代码更新后，重新运行构建脚本即可生成新的 DMG。