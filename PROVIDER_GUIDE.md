# AI Provider Switcher - 提供商配置指南

## 🎯 提供商适配说明

系统已完全适配不同提供商的特殊要求，自动为每个提供商设置正确的环境变量。

## 📋 当前配置的提供商

### 1. Claude Nekro (`claude_code_nexus`)
- **URL**: https://claude.nekro.ai
- **特点**: 内置模型映射，使用特殊认证方式
- **环境变量**:
  ```bash
  export ANTHROPIC_BASE_URL="https://claude.nekro.ai"
  export ANTHROPIC_AUTH_TOKEN="ak-xxx..."  # 注意：使用 AUTH_TOKEN
  # 无需设置模型名称
  ```
- **使用方式**: `claude` 直接使用，模型由服务端自动选择

### 2. OpenRouter (`openrouter_yovy`) 
- **URL**: https://cc.yovy.app
- **特点**: 需要明确指定模型，支持多种模型选择
- **环境变量**:
  ```bash
  export ANTHROPIC_BASE_URL="https://cc.yovy.app"
  export ANTHROPIC_API_KEY="sk-xxx..."
  export ANTHROPIC_MODEL="moonshotai/kimi-k2:free"
  export ANTHROPIC_SMALL_FAST_MODEL="moonshotai/kimi-k2:free"
  ```
- **使用方式**: `claude` 使用指定的模型

### 3. Moonshot (`moonshot`)
- **URL**: https://api.moonshot.cn/v1  
- **特点**: 兼容Claude格式，模型名称可选
- **环境变量**:
  ```bash
  export ANTHROPIC_BASE_URL="https://api.moonshot.cn/v1"
  export ANTHROPIC_API_KEY="sk-xxx..."
  # 模型名称可选，不设置也能正常工作
  ```
- **使用方式**: `claude` 直接使用

### 4. 九万里国学 (`ai-codewith`)
- **URL**: https://api.jiuwanliguoxue.com/
- **特点**: 标准Anthropic兼容API
- **环境变量**:
  ```bash
  export ANTHROPIC_BASE_URL="https://api.jiuwanliguoxue.com/"
  export ANTHROPIC_API_KEY="sk-xxx..."
  export ANTHROPIC_MODEL="claude-sonnet-4-20250514"
  export ANTHROPIC_SMALL_FAST_MODEL="claude-sonnet-4-20250514"
  ```
- **使用方式**: `claude` 使用指定模型

## 🔄 自动适配逻辑

系统会根据提供商类型自动设置正确的环境变量：

### Claude Nekro 特殊处理
```python
if provider.name == "claude_code_nexus":
    env_vars["ANTHROPIC_AUTH_TOKEN"] = provider.api_key
    # 不设置模型名称，使用内置映射
```

### OpenRouter 特殊处理  
```python
elif provider.name == "openrouter_yovy":
    env_vars["ANTHROPIC_API_KEY"] = provider.api_key
    env_vars["ANTHROPIC_MODEL"] = provider.model
    env_vars["ANTHROPIC_SMALL_FAST_MODEL"] = provider.small_fast_model
```

### Moonshot 特殊处理
```python
elif provider.type == ProviderType.MOONSHOT:
    env_vars["ANTHROPIC_API_KEY"] = provider.api_key
    # 模型名称可选，设置为"auto"则不添加到环境变量
    if provider.model and provider.model != "auto":
        env_vars["ANTHROPIC_MODEL"] = provider.model
```

## ✅ 使用建议

### 推荐使用顺序（按响应速度）:
1. **ai-codewith** - 最快响应 (~0.3s)
2. **moonshot** - 中等响应 (~0.7s) 
3. **claude_code_nexus** - 较慢但稳定 (~1.5s)

### 快速启动方式:
```bash
# 自动选择最佳提供商
python3 start_claude.py

# 在TideLog项目中启动  
python3 start_claude.py TideLog

# 手动选择提供商（如果需要Claude Nekro的特殊功能）
python3 test_claude_nekro.py
```

## 🛠️ 配置验证

运行以下命令验证配置是否正确：

```bash
# 测试所有提供商配置
python3 test_providers.py

# 专门测试Claude Nekro
python3 test_claude_nekro.py

# 验证配置文件
python3 config_manager.py validate
```

## 💡 关键优势

1. **自动适配**: 无需手动配置不同提供商的环境变量
2. **智能选择**: 自动选择响应最快的健康提供商  
3. **兼容性**: 完美兼容每个提供商的特殊要求
4. **模型管理**: 
   - Claude Nekro: 无需指定模型（内置映射）
   - OpenRouter: 必须指定模型名称
   - Moonshot: 模型可选（兼容Claude格式）
   - 其他: 标准模型配置

## 🔧 故障排除

### 问题: Claude Nekro 连接失败
- 确保使用 `ANTHROPIC_AUTH_TOKEN` 而不是 `ANTHROPIC_API_KEY`
- 检查是否设置了不必要的模型名称

### 问题: OpenRouter 模型错误
- 确保在配置中明确指定了正确的模型名称
- 检查 https://openrouter.ai/models 获取可用模型列表

### 问题: Moonshot 兼容性
- 可以不设置模型名称，使用默认配置
- 或者设置为 "auto" 让系统自动处理

现在您的AI Provider Switcher已完全适配所有提供商的特殊要求！🎉