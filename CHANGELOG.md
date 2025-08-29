# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-28

### Added
- **Initial Release** - Easy Claude Code AI Provider Switcher
- **Beautiful GUI** - Modern tkinter-based interface with left-right balanced layout
- **One-Click Switching** - Switch between AI providers with a single click
- **Real-time Health Monitoring** - Automatic health checking for all providers
- **Cross-platform Support** - Windows, macOS, and Linux compatibility
- **Smart Environment Management** - Automatic environment variable configuration
- **Project Directory Management** - Select and browse project directories
- **Terminal Integration** - Automatic terminal launch with configured environment
- **10+ AI Provider Support** - OpenRouter, Moonshot, DeepSeek, Custom Anthropic, etc.

### Features
- **Provider Health Checking** - Concurrent health monitoring with response time tracking
- **Priority-based Sorting** - Intelligent provider selection based on health and speed
- **Configuration Management** - JSON-based configuration with validation
- **Custom Headers Support** - Support for providers requiring special HTTP headers
- **Environment Variable Isolation** - Clean environment setup for each provider
- **Cross-desktop Terminal Support** - Auto-detection of available terminal emulators

### Supported Providers
- OpenRouter (Smart routing)
- Custom Anthropic (Custom Claude endpoints)
- Moonshot AI (Moon Dark Side)
- DeepSeek AI
- Zhipu AI (GLM models)
- Baichuan AI
- Official Anthropic
- Azure OpenAI
- Google Gemini
- Local Ollama

### Technical Details
- **Python 3.8+** compatibility
- **Async HTTP requests** with aiohttp
- **Graceful error handling** with detailed logging
- **Cross-platform terminal detection**
- **Intelligent health check endpoints**
- **Configurable timeouts and retries**

### GUI Features
- **Left Panel** - AI Provider management with status indicators
- **Right Panel** - Project directory selection, status display, and terminal operations
- **Real-time Updates** - Live provider status monitoring
- **One-Click Launch** - Automatic provider activation + terminal launch
- **Folder Browser** - Easy project directory selection
- **Status Display** - Current provider and environment variables view

### Documentation
- Comprehensive README with installation and usage guides
- Provider configuration examples
- Troubleshooting guide
- Contributing guidelines
- MIT License