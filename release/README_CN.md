# Easy Claude Code

🚀 **为 Claude Code 提供简单易用的 AI 提供商切换工具，配有精美 GUI 界面**

一个智能的 AI 提供商切换器，支持通过 Cloudflare Workers 代理和直接端点访问各种 Claude 兼容的 API，具备智能健康监控和自动环境变量管理功能。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ 功能特性

### 🎯 核心功能
- **🔄 一键切换** - 单击即可切换 AI 提供商
- **📊 实时健康监控** - 自动健康检查和响应时间跟踪
- **🎨 精美界面** - 简洁直观的左右平衡布局界面
- **🌍 跨平台支持** - 支持 Windows、macOS 和 Linux
- **🔧 智能环境管理** - 自动配置环境变量
- **💾 设置持久化** - 项目目录和偏好设置自动保存

### 🔗 支持的 API 服务

#### 🌐 Cloudflare Workers 代理服务
- **🔀 [cc.yovy.app](https://cc.yovy.app/)** - OpenRouter API 代理
  - 通过 OpenRouter 访问多种 AI 模型
  - 需要 OpenRouter API 密钥（`sk-or-v1-` 前缀）
  - 支持 Claude、GPT、Llama 等多种模型

- **🧠 [claude.nekro.ai](https://claude.nekro.ai/)** - 多提供商代理
  - **通义千问**（阿里巴巴）
  - **智谱 AI**（智谱清言/GLM 模型）
  - **Google Gemini**（Gemini Pro/Flash）
  - **以及更多 AI 提供商**
  - 使用 `ak-` 前缀的 API 密钥

#### 🎯 直连 API 端点
- **🌙 月之暗面** - Claude 兼容的直连 API
  - 月之暗面的 Kimi 模型
  - 原生 Claude API 格式支持
  - 高速中文语言处理

- **🏢 Anthropic 官方** - Claude 官方直连 API
  - Claude 3.5 Sonnet/Haiku
  - 官方 API，功能完整支持
  - 需要官方 Anthropic API 密钥

- **🔧 任何 Claude 兼容 API** - 自定义端点
  - 支持自托管的 Claude 兼容服务
  - 灵活配置自定义提供商
  - 自动检测 API 功能

## 🖼️ 界面截图

### 主界面
```
┌─────────────────────────────────────────────────────────────────┐
│                      Easy Claude Code                           │
├─────────────────────────────────┬───────────────────────────────┤
│        🤖 AI 提供商管理          │       📁 项目目录            │
│                                │                               │
│ 提供商名称      │ 类型  │ 状态  │ ┌───────────────────────────┐ │
│ yovy-openrouter│ 代理  │   ✅  │ │ [我的项目     ▼] [📂 浏览] │ │
│ nekro-claude   │ 代理  │   ✅  │ └───────────────────────────┘ │
│ moonshot-direct│ 直连  │   ✅  │                               │
│                                │ ┌───────────────────────────┐ │
│ [🔄 刷新] [⚙️ 配置]              │ │    📊 当前状态            │ │
│                                │ │ 激活: nekro-claude        │ │
│                                │ │ ANTHROPIC_AUTH_TOKEN=ak-..│ │
│                                │ └───────────────────────────┘ │
│                                │                               │
│                                │ ┌───────────────────────────┐ │
│                                │ │    🚀 终端操作            │ │
│                                │ │                           │ │
│                                │ │    🚀 一键启动            │ │
│                                │ └───────────────────────────┘ │
└─────────────────────────────────┴───────────────────────────────┘
```

## 🚀 快速开始

### 前置条件
- Python 3.8+ 
- 已安装并配置 Claude Code
- 来自支持服务的 API 密钥

### 安装

```bash
# 克隆仓库
git clone https://github.com/username/easy-claude-code.git
cd easy-claude-code

# 安装依赖
pip install aiohttp

# 运行应用
python run.py
```

### 获取 API 密钥

#### OpenRouter 通过 cc.yovy.app
1. 访问 [OpenRouter](https://openrouter.ai/) 并创建账户
2. 生成 API 密钥（以 `sk-or-v1-` 开头）
3. 使用 `https://cc.yovy.app` 作为基础 URL
4. 选择模型如 `anthropic/claude-3.5-sonnet`

#### 多提供商通过 claude.nekro.ai
1. 获取 claude.nekro.ai 服务的访问权限
2. 获得 API 密钥（以 `ak-` 开头）
3. 使用 `https://claude.nekro.ai` 作为基础 URL
4. 将模型设置为 `auto` 进行自动选择

#### 月之暗面（直连）
1. 在 [月之暗面](https://moonshot.cn/) 注册账户
2. 生成 API 密钥（以 `sk-` 开头）
3. 使用 `https://api.moonshot.cn/anthropic/` 作为基础 URL
4. 兼容 Claude API 格式

### 首次设置

1. **启动应用**:
   ```bash
   python run.py
   ```

2. **配置提供商**:
   - 复制 `providers.example.json` 为 `providers.json`
   - 编辑并填入实际的 API 密钥
   - 或使用 GUI 的"添加提供商"按钮

3. **开始使用**:
   - 从左侧面板选择 AI 提供商
   - 选择您的项目目录
   - 点击"🚀 一键启动"开始编程！

## 📋 配置说明

### 提供商配置

编辑 `providers.json` 文件，填入您的 API 密钥：

```json
{
  "providers": [
    {
      "name": "yovy-openrouter",
      "type": "openrouter", 
      "base_url": "https://cc.yovy.app",
      "api_key": "sk-or-v1-你的实际密钥",
      "model": "anthropic/claude-3.5-sonnet",
      "small_fast_model": "anthropic/claude-3.5-haiku",
      "priority": 1
    },
    {
      "name": "nekro-multi",
      "type": "custom_anthropic",
      "base_url": "https://claude.nekro.ai", 
      "api_key": "ak-你的实际密钥",
      "model": "auto",
      "small_fast_model": "auto",
      "priority": 2
    }
  ]
}
```

### 环境变量

Easy Claude Code 自动管理以下环境变量：

- `ANTHROPIC_API_KEY` - 用于 OpenRouter 和直连 API
- `ANTHROPIC_AUTH_TOKEN` - 用于 claude.nekro.ai 和自定义端点  
- `ANTHROPIC_BASE_URL` - 提供商的基础 URL
- `ANTHROPIC_MODEL` - 模型名称（需要时）
- `ANTHROPIC_SMALL_FAST_MODEL` - 快速模型用于简单任务

## 💡 使用指南

### 基本工作流程

1. **选择提供商**: 从代理或直连 API 提供商中选择
2. **选择项目**: 选择或浏览到您的项目目录  
3. **启动**: 点击"🚀 一键启动"进行即时设置

### 提供商选择指南

#### 何时使用 **cc.yovy.app**（OpenRouter 代理）:
- ✅ 需要访问多种模型提供商
- ✅ 想要比较不同的 AI 模型
- ✅ 需要高可用性和负载均衡
- ✅ 有 OpenRouter 账户和积分/订阅

#### 何时使用 **claude.nekro.ai**（多提供商代理）:
- ✅ 需要中文 AI 模型（通义、智谱）
- ✅ 想要访问 Gemini 模型
- ✅ 偏好多提供商的统一 API
- ✅ 寻找成本效益解决方案

#### 何时使用**直连 API**:
- ✅ 有官方 Anthropic 账户和 Claude API 访问权限
- ✅ 有月之暗面账户用于中文语言任务
- ✅ 自定义或自托管的 Claude 兼容服务
- ✅ 需要完全控制和最低延迟

## 🔧 技术细节

### 架构

- **`provider_switch.py`** - 核心提供商管理和健康检查
- **`gui_switcher_v2.py`** - 基于 tkinter 的现代 GUI 界面
- **`terminal_launcher.py`** - 跨平台终端启动器
- **`providers.json`** - 提供商和项目的配置文件

### 健康检查算法

1. **并发检查** - 同时检查所有提供商
2. **代理感知端点** - 为每种服务类型使用合适的测试 URL
3. **容错状态码** - 接受 200/401/403/404 作为健康状态（服务器响应）
4. **超时处理** - 可配置的超时和优雅失败

### API 兼容性

| 提供商类型 | 身份验证 | 模型选择 | 特殊功能 |
|-----------|---------|---------|---------|
| cc.yovy.app | `sk-or-v1-` 密钥 | OpenRouter 模型 | 多提供商路由 |
| claude.nekro.ai | `ak-` 密钥 | 自动检测 | 中文 AI 模型 |
| 月之暗面 | `sk-` 密钥 | Kimi 模型 | 中文语言优化 |
| 官方 | `sk-ant-` 密钥 | Claude 模型 | 完整 Claude 功能 |

## 🤝 贡献

我们欢迎贡献！以下是您可以提供帮助的方式：

### 添加新的代理服务
1. 向 `ProviderType` 枚举添加提供商类型
2. 为新服务更新健康检查逻辑
3. 添加配置示例
4. 更新文档

### 报告问题
- 使用 GitHub Issues 报告错误
- 包含 API 提供商和错误消息
- 提供重现步骤

## 📝 许可证

本项目采用 MIT 许可证 - 详情请参见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- **Claude Code 团队** - 提供了出色的 AI 编程助手
- **OpenRouter** - 提供多种 AI 模型访问
- **Cloudflare Workers** - 启用代理服务
- **所有代理服务提供商** - 让 AI 模型更易访问

## 🆘 支持

- **文档**: 查看本 README 和 [提供商指南](PROVIDER_GUIDE.md)
- **问题**: [GitHub Issues](https://github.com/username/easy-claude-code/issues)
- **讨论**: [GitHub Discussions](https://github.com/username/easy-claude-code/discussions)

## ⚠️ 重要提醒

- **代理服务**: 此工具中的大多数提供商使用 Cloudflare Workers 代理，而非直接官方 API
- **API 密钥**: 每个服务需要其自己的 API 密钥格式和注册流程  
- **速率限制**: 不同提供商有不同的速率限制和使用政策
- **费用**: 大量使用前请检查各提供商的定价
- **合规性**: 确保您的使用符合各提供商的服务条款

## 🌟 使用建议

### 国内用户推荐顺序
1. **claude.nekro.ai** - 支持中文模型，响应速度快
2. **月之暗面直连** - 中文处理能力强，国内访问稳定
3. **cc.yovy.app** - 模型选择丰富，适合模型对比
4. **官方 Anthropic** - 功能最全，但需要国外网络

### 成本考虑
- **claude.nekro.ai** - 通常成本较低，适合日常使用
- **月之暗面** - 中文任务性价比高
- **OpenRouter** - 按使用付费，适合偶发需求
- **官方 API** - 功能最全但成本相对较高

---

**⭐ 如果您觉得 Easy Claude Code 有用，请给我们点个星！**

用 ❤️ 为 Claude Code 社区制作