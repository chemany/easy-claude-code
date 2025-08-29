# Easy Claude Code - Linux 单文件版本安装指南

🚀 **一键启动的 Linux 单文件可执行版本**

## 📦 包含文件

- `easy-claude-code` - 主程序可执行文件 (18MB)
- `providers.example.json` - API提供商配置示例
- `README.md` - 项目说明 (英文)
- `README_CN.md` - 项目说明 (中文)
- `LICENSE` - MIT 开源许可证
- `INSTALL.md` - 本安装说明

## 🚀 快速安装

### 1. 下载和准备

```bash
# 下载发布包到任意目录
cd ~/Downloads
unzip easy-claude-code-linux.zip
cd easy-claude-code-linux/

# 或者如果是从GitHub下载
git clone https://github.com/username/easy-claude-code.git
cd easy-claude-code/release/
```

### 2. 配置API提供商

```bash
# 复制配置示例为实际配置文件
cp providers.example.json providers.json

# 编辑配置文件，填入您的真实API密钥
nano providers.json
# 或使用其他编辑器: vim, gedit, kate, etc.
```

**重要**: 将示例中的API密钥替换为您的真实密钥：
- `sk-or-v1-your-openrouter-key-here` → 您的OpenRouter密钥
- `ak-your-nekro-api-key-here` → 您的claude.nekro.ai密钥
- `sk-your-moonshot-key-here` → 您的月之暗面密钥

### 3. 启动程序

#### 方法一：双击启动 (推荐)
1. 在文件管理器中找到 `easy-claude-code` 文件
2. 双击运行
3. 如果提示需要权限，右键选择"运行"或"作为程序运行"

#### 方法二：终端启动
```bash
# 确保文件具有执行权限
chmod +x easy-claude-code

# 启动程序
./easy-claude-code
```

## 🔧 系统要求

### 最低要求
- **操作系统**: Linux x86_64 (64位)
- **桌面环境**: 支持 GTK/Tkinter 的桌面环境
- **内存**: 至少 256MB 可用内存
- **磁盘空间**: 20MB 用于程序文件

### 测试过的系统
- ✅ Ubuntu 20.04/22.04/24.04
- ✅ Debian 11/12
- ✅ CentOS 8/9
- ✅ Fedora 38+
- ✅ openSUSE Leap 15.5+
- ✅ Arch Linux
- ✅ Linux Mint 20+

### 支持的桌面环境
- ✅ GNOME (Ubuntu 默认)
- ✅ XFCE (Xubuntu)
- ✅ KDE Plasma (Kubuntu)
- ✅ MATE (Ubuntu MATE)
- ✅ LXQt/LXDE
- ✅ Cinnamon (Linux Mint)
- ✅ Deepin Desktop

## 🛠️ 终端检测

程序自动检测可用终端，支持以下终端模拟器：

### Ubuntu/Debian 系统
- `x-terminal-emulator` (系统默认)
- `sensible-terminal` (智能选择器)
- `gnome-terminal` (GNOME 默认)

### 其他终端
- `xfce4-terminal`, `konsole`, `mate-terminal`
- `tilix`, `terminator`, `alacritty`, `kitty`
- `xterm`, `urxvt`, `sakura`, `qterminal`

## 📁 配置说明

### providers.json 结构

```json
{
  "project_directories": [
    {
      "name": "我的项目",
      "path": "/home/username/my-project", 
      "description": "项目描述"
    }
  ],
  "providers": [
    {
      "name": "提供商名称",
      "type": "提供商类型",
      "base_url": "API基础URL",
      "api_key": "您的API密钥",
      "model": "模型名称",
      "priority": 1
    }
  ]
}
```

### 支持的提供商类型
- `openrouter` - OpenRouter API 代理
- `custom_anthropic` - 自定义 Claude 兼容 API
- `moonshot` - 月之暗面直连 API
- `official_anthropic` - Anthropic 官方 API

## 🚨 安全注意事项

### ⚠️ 重要安全提醒

1. **API密钥保护**
   - 不要在公开场所显示 `providers.json` 文件
   - 不要将包含真实API密钥的配置文件提交到版本控制
   - 定期轮换API密钥

2. **文件权限**
   ```bash
   # 设置配置文件只有用户可读写
   chmod 600 providers.json
   
   # 设置程序文件可执行
   chmod +x easy-claude-code
   ```

3. **网络安全**
   - 仅在可信网络环境下使用
   - 避免在公共WiFi下传输敏感数据
   - 检查防火墙设置允许程序网络访问

## 🔧 故障排除

### 常见问题

#### 1. 双击无反应
```bash
# 检查文件权限
ls -la easy-claude-code

# 确保有执行权限
chmod +x easy-claude-code

# 在终端中运行查看错误信息
./easy-claude-code
```

#### 2. GUI无法显示
```bash
# 检查显示环境变量
echo $DISPLAY

# 如果通过SSH连接，确保启用X11转发
ssh -X username@hostname
```

#### 3. 缺少依赖库
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-tk libgtk-3-0

# CentOS/RHEL
sudo yum install tkinter gtk3

# Fedora
sudo dnf install python3-tkinter gtk3
```

#### 4. 终端检测失败
程序会显示检测到的终端列表，如果没有找到合适的终端：
```bash
# 安装一个支持的终端
sudo apt install gnome-terminal  # Ubuntu
sudo yum install gnome-terminal  # CentOS
```

### 获取支持

- **文档**: 查看 README.md 和 README_CN.md
- **问题报告**: GitHub Issues
- **讨论**: GitHub Discussions

## 📊 性能优化

### 内存使用优化
- 程序启动后占用约 50-80MB 内存
- 可以通过关闭不需要的提供商来减少内存使用

### 启动速度优化
- 首次启动可能需要2-3秒初始化
- 后续启动通常在1秒内完成
- SSD硬盘可以显著提升启动速度

## 🌟 使用技巧

1. **快速切换**: 使用数字键1-9快速选择提供商
2. **健康检查**: 启动时自动检查所有提供商状态
3. **项目管理**: 可以保存多个项目目录，便于快速切换
4. **终端集成**: 自动配置环境变量并启动终端

---

**🎉 享受使用 Easy Claude Code！**

如有问题，请查看 README 文档或提交 Issue。