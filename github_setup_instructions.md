# GitHub 发布指南

## 第一步：GitHub CLI 认证

请在终端中运行以下命令进行GitHub认证：

```bash
cd /home/jason/code/easy-claude-code
gh auth login
```

选择：
1. GitHub.com
2. HTTPS
3. Login with a web browser（或使用Personal Access Token）

## 第二步：创建GitHub仓库并推送

认证完成后，运行以下命令：

```bash
# 创建GitHub仓库（公开）
gh repo create easy-claude-code --public --description "🚀 Easily switch between different AI providers for Claude Code with a beautiful GUI. Single-file Linux executable with cross-platform terminal support."

# 添加远程仓库
git remote add origin https://github.com/$(gh api user --jq .login)/easy-claude-code.git

# 推送代码
git push -u origin main
```

## 第三步：创建Release和上传文件

```bash
# 创建Release
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

如有问题，请查看 [INSTALL.md](https://github.com/username/easy-claude-code/blob/main/release/INSTALL.md) 获取详细安装说明。
EOF
)" \
  releases/easy-claude-code-linux-v1.0.0.tar.gz \
  releases/easy-claude-code-linux-v1.0.0.zip \
  releases/easy-claude-code-linux-v1.0.0.tar.gz.sha256 \
  releases/easy-claude-code-linux-v1.0.0.zip.sha256
```

## 完成！

仓库地址将是：`https://github.com/$(gh api user --jq .login)/easy-claude-code`

用户可以通过以下方式下载：
- 访问 Releases 页面下载单文件可执行版本
- 或者克隆仓库自己构建：`git clone` 然后 `./build_linux_binary.sh`