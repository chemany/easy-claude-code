# Easy Claude Code

🚀 **Easily switch between different AI providers for Claude Code with a beautiful GUI**

A smart AI provider switcher that supports various Claude-compatible APIs through Cloudflare Workers proxies and direct endpoints, with intelligent health monitoring and automatic environment variable management.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ Features

### 🎯 Core Functionality
- **🔄 One-Click Switching** - Switch between AI providers with a single click
- **📊 Real-time Health Monitoring** - Automatic health checking with response time tracking
- **🎨 Beautiful GUI** - Clean, intuitive interface with left-right balanced layout
- **🌍 Cross-platform Support** - Works on Windows, macOS, and Linux
- **🔧 Smart Environment Management** - Automatic environment variable configuration
- **💾 Persistent Settings** - Project directories and preferences are saved automatically

### 🔗 Supported API Services

#### 🌐 Cloudflare Workers Proxies
- **🔀 [cc.yovy.app](https://cc.yovy.app/)** - OpenRouter API proxy
  - Access to multiple AI models through OpenRouter
  - Requires OpenRouter API key with `sk-or-v1-` prefix
  - Supports Claude, GPT, Llama, and other models

- **🧠 [claude.nekro.ai](https://claude.nekro.ai/)** - Multi-provider proxy
  - **Tongyi Qianwen** (阿里通义千问)
  - **Zhipu AI** (智谱清言/GLM models)
  - **Google Gemini** (Gemini Pro/Flash)
  - **And more AI providers**
  - Uses `ak-` prefixed API keys

#### 🎯 Direct API Endpoints
- **🌙 Moonshot AI** - Direct Claude-compatible API
  - Moon Dark Side's Kimi models
  - Native Claude API format support
  - High-speed Chinese language processing

- **🏢 Official Anthropic** - Direct Claude API
  - Claude 3.5 Sonnet/Haiku
  - Official API with full feature support
  - Requires official Anthropic API key

- **🔧 Any Claude-Compatible API** - Custom endpoints
  - Support for self-hosted Claude-compatible services
  - Flexible configuration for custom providers
  - Auto-detection of API capabilities

## 🖼️ Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────────────┐
│                      Easy Claude Code                           │
├─────────────────────────────────┬───────────────────────────────┤
│        🤖 AI Provider 管理      │       📁 Project Directory   │
│                                │                               │
│ Provider       │ Type  │ Status│ ┌───────────────────────────┐ │
│ yovy-openrouter│ proxy │   ✅  │ │ [My Project   ▼] [📂 Browse]│ │
│ nekro-claude   │ proxy │   ✅  │ └───────────────────────────┘ │
│ moonshot-direct│ direct│   ✅  │                               │
│                                │ ┌───────────────────────────┐ │
│ [🔄 Refresh] [⚙️ Config]        │ │    📊 Current Status      │ │
│                                │ │ Active: nekro-claude      │ │
│                                │ │ ANTHROPIC_AUTH_TOKEN=ak-..│ │
│                                │ └───────────────────────────┘ │
│                                │                               │
│                                │ ┌───────────────────────────┐ │
│                                │ │    🚀 Terminal Actions   │ │
│                                │ │                           │ │
│                                │ │    🚀 One-Click Launch   │ │
│                                │ └───────────────────────────┘ │
└─────────────────────────────────┴───────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- Claude Code installed and configured
- API keys from supported services

### Installation

```bash
# Clone the repository
git clone https://github.com/username/easy-claude-code.git
cd easy-claude-code

# Install dependencies
pip install aiohttp

# Run the application
python run.py
```

### Getting API Keys

#### For OpenRouter via cc.yovy.app
1. Visit [OpenRouter](https://openrouter.ai/) and create an account
2. Generate an API key (starts with `sk-or-v1-`)
3. Use `https://cc.yovy.app` as the base URL
4. Select models like `anthropic/claude-3.5-sonnet`

#### For Multi-provider via claude.nekro.ai
1. Get access to claude.nekro.ai service
2. Obtain an API key (starts with `ak-`)
3. Use `https://claude.nekro.ai` as the base URL
4. Set model to `auto` for automatic selection

#### For Moonshot AI (Direct)
1. Register at [Moonshot AI](https://moonshot.cn/)
2. Generate API key (starts with `sk-`)
3. Use `https://api.moonshot.cn/anthropic/` as base URL
4. Compatible with Claude API format

### First Time Setup

1. **Launch the application**:
   ```bash
   python run.py
   ```

2. **Configure your providers**:
   - Copy `providers.example.json` to `providers.json`
   - Edit with your actual API keys
   - Or use the GUI's "Add Provider" button

3. **Start using**:
   - Select an AI provider from the left panel
   - Choose your project directory
   - Click "🚀 One-Click Launch" to start coding!

## 📋 Configuration

### Provider Configuration

Edit `providers.json` with your API keys:

```json
{
  "providers": [
    {
      "name": "yovy-openrouter",
      "type": "openrouter", 
      "base_url": "https://cc.yovy.app",
      "api_key": "sk-or-v1-your-actual-key",
      "model": "anthropic/claude-3.5-sonnet",
      "small_fast_model": "anthropic/claude-3.5-haiku",
      "priority": 1
    },
    {
      "name": "nekro-multi",
      "type": "custom_anthropic",
      "base_url": "https://claude.nekro.ai", 
      "api_key": "ak-your-actual-key",
      "model": "auto",
      "small_fast_model": "auto",
      "priority": 2
    }
  ]
}
```

### Environment Variables

Easy Claude Code automatically manages these environment variables:

- `ANTHROPIC_API_KEY` - For OpenRouter and direct APIs
- `ANTHROPIC_AUTH_TOKEN` - For claude.nekro.ai and custom endpoints  
- `ANTHROPIC_BASE_URL` - Provider's base URL
- `ANTHROPIC_MODEL` - Model name (when required)
- `ANTHROPIC_SMALL_FAST_MODEL` - Fast model for simple tasks

## 💡 Usage

### Basic Workflow

1. **Select Provider**: Choose from proxy or direct API providers
2. **Choose Project**: Select or browse to your project directory  
3. **Launch**: Click "🚀 One-Click Launch" for instant setup

### Provider Selection Guide

#### When to use **cc.yovy.app** (OpenRouter Proxy):
- ✅ Need access to multiple model providers
- ✅ Want to compare different AI models
- ✅ Require high availability and load balancing
- ✅ OpenRouter account with credits/subscription

#### When to use **claude.nekro.ai** (Multi-provider Proxy):
- ✅ Need Chinese AI models (Tongyi, Zhipu)
- ✅ Want to access Gemini models
- ✅ Prefer unified API for multiple providers
- ✅ Looking for cost-effective solutions

#### When to use **Direct APIs**:
- ✅ Official Anthropic account with Claude API access
- ✅ Moonshot AI account for Chinese language tasks
- ✅ Custom or self-hosted Claude-compatible services
- ✅ Need full control and lowest latency

## 🔧 Technical Details

### Architecture

- **`provider_switch.py`** - Core provider management and health checking
- **`gui_switcher_v2.py`** - Modern GUI interface with tkinter
- **`terminal_launcher.py`** - Cross-platform terminal launcher
- **`providers.json`** - Configuration file for providers and projects

### Health Checking Algorithm

1. **Concurrent Checks** - All providers checked simultaneously
2. **Proxy-Aware Endpoints** - Uses appropriate test URLs for each service type
3. **Tolerant Status Codes** - Accepts 200/401/403/404 as healthy (server responsive)
4. **Timeout Handling** - Configurable timeouts with graceful failure

### API Compatibility

| Provider Type | Authentication | Model Selection | Special Features |
|---------------|----------------|-----------------|------------------|
| cc.yovy.app | `sk-or-v1-` key | OpenRouter models | Multi-provider routing |
| claude.nekro.ai | `ak-` key | Auto-detection | Chinese AI models |
| Moonshot | `sk-` key | Kimi models | Chinese language optimized |
| Official | `sk-ant-` key | Claude models | Full Claude features |

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Adding New Proxy Services
1. Add provider type to `ProviderType` enum
2. Update health check logic for the new service
3. Add configuration examples
4. Update documentation

### Reporting Issues
- Use GitHub Issues for bug reports
- Include API provider and error messages
- Provide steps to reproduce

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Claude Code Team** - For the amazing AI coding assistant
- **OpenRouter** - For providing access to multiple AI models
- **Cloudflare Workers** - For enabling proxy services
- **All Proxy Service Providers** - For making AI models more accessible

## 🆘 Support

- **Documentation**: Check this README and [Provider Guide](PROVIDER_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/username/easy-claude-code/issues)
- **Discussions**: [GitHub Discussions](https://github.com/username/easy-claude-code/discussions)

## ⚠️ Important Notes

- **Proxy Services**: Most providers in this tool use Cloudflare Workers proxies, not direct official APIs
- **API Keys**: Each service requires its own API key format and registration process  
- **Rate Limits**: Different providers have different rate limits and usage policies
- **Costs**: Check each provider's pricing before heavy usage
- **Compliance**: Ensure your usage complies with each provider's terms of service

---

**⭐ If you find Easy Claude Code helpful, please give it a star!**

Made with ❤️ for the Claude Code community