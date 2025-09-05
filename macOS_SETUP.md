# macOS 快速开始指南

## 🍎 macOS 用户专用说明

### 方法一：一键运行（推荐）

1. **下载项目**
   ```bash
   # 在终端中运行（需要 Git）
   git clone https://github.com/chemany/easy-claude-code.git
   cd easy-claude-code
   ```

2. **运行启动脚本**
   ```bash
   ./run_macos.sh
   ```

   脚本会自动：
   - ✅ 检查系统要求
   - ✅ 安装必要依赖
   - ✅ 创建配置文件
   - ✅ 启动图形界面

### 方法二：手动配置

1. **检查 Python**
   ```bash
   python3 --version
   # 需要 Python 3.8 或更高版本
   ```

2. **安装依赖**
   ```bash
   pip3 install aiohttp
   ```

3. **配置 API Keys**
   ```bash
   # 创建配置目录
   mkdir -p ~/.config/easy-claude-code
   
   # 复制配置文件
   cp providers.example.json ~/.config/easy-claude-code/providers.json
   
   # 编辑配置
   nano ~/.config/easy-claude-code/providers.json
   ```

4. **运行程序**
   ```bash
   python3 run.py
   ```

### 📁 配置文件位置

在 macOS 上，配置文件位于：
```
~/.config/easy-claude-code/providers.json
```

### 🚀 首次运行

1. 运行脚本后，会提示您编辑配置文件
2. 将示例 API keys 替换为您的真实 keys：
   - `sk-or-v1-your-openrouter-key-here` → 您的 OpenRouter API key
   - `ak-your-nekro-api-key-here` → 您的 Claude Nekro API key
3. 保存文件后按回车继续

### 🛠️ 获取 API Keys

#### OpenRouter
1. 访问 [OpenRouter.ai](https://openrouter.ai)
2. 注册账户
3. 生成 API key（以 `sk-or-v1-` 开头）

#### Claude Nekro
1. 访问 [claude.nekro.ai](https://claude.nekro.ai)
2. 获取访问权限
3. 获取 API key（以 `ak-` 开头）

### 📱 zsh 用户说明

- 脚本完全兼容 zsh shell
- 支持 `${XDG_CONFIG_HOME}` 环境变量
- 使用标准 macOS 路径格式

### 🔧 故障排除

#### 问题：无法打开应用
**解决**：macOS 安全机制阻止
```bash
# 在系统设置中：
系统设置 → 隐私与安全性 → 安全性
允许从以下位置下载的 App：App Store 和被认可的开发者
```

#### 问题：Python 未找到
**解决**：安装 Python
```bash
# 使用 Homebrew（推荐）
brew install python3

# 或从官网下载
https://www.python.org/downloads/macos/
```

#### 问题：依赖安装失败
**解决**：
```bash
# 使用 pip3
pip3 install --user aiohttp

# 或升级 pip
pip3 install --upgrade pip
```

### 🎯 使用技巧

1. **创建桌面快捷方式**
   ```bash
   # 创建桌面快捷命令
   echo 'alias claude-code="cd ~/path/to/easy-claude-code && ./run_macos.sh"' >> ~/.zshrc
   source ~/.zshrc
   ```

2. **自动启动**
   - 将 `Easy Claude Code.app` 拖到 Dock
   - 或添加到登录项

### 💡 提示

- 首次运行可能需要几秒钟加载
- GUI 界面支持中文显示
- 所有配置会自动保存
- 支持多个 AI 提供商切换

---

享受使用 Easy Claude Code！🎉