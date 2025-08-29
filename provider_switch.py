#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easy Claude Code - AI Provider Switcher Core Module

Easily switch between different AI providers for Claude Code with intelligent health monitoring.
Supports seamless switching between various AI service providers through environment variable management.

Repository: https://github.com/username/easy-claude-code
License: MIT
"""

import asyncio
import aiohttp
import json
import os
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class ProviderType(Enum):
    OPENROUTER = "openrouter"
    CUSTOM_ANTHROPIC = "custom_anthropic"
    DEEPSEEK = "deepseek"
    MOONSHOT = "moonshot"
    ZHIPU = "zhipu"
    BAICHUAN = "baichuan"
    OFFICIAL_ANTHROPIC = "official_anthropic"
    AZURE_OPENAI = "azure_openai"
    GEMINI = "gemini"
    LOCAL_OLLAMA = "local_ollama"


@dataclass
class ProviderConfig:
    name: str
    type: ProviderType
    base_url: str
    api_key: str
    model: str
    small_fast_model: str
    custom_headers: Optional[Dict[str, str]] = None
    priority: int = 1
    max_retries: int = 3
    timeout: float = 30.0

@dataclass
class ProjectDirectory:
    name: str
    path: str
    description: str = ""


@dataclass
class HealthStatus:
    provider_name: str
    is_healthy: bool
    response_time: float
    last_check: float
    error_message: Optional[str] = None


class AIProviderError(Exception):
    """AI提供者相关的错误"""
    pass


class AIProviderSwitcher:
    """AI提供者自动切换器"""
    
    def __init__(self, config_file: str = "providers.json"):
        self.config_file = config_file
        self.providers: List[ProviderConfig] = []
        self.project_directories: List[ProjectDirectory] = []
        self.health_status: Dict[str, HealthStatus] = {}
        self.current_provider: Optional[str] = None
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
                # 加载项目目录
                for dir_data in config_data.get('project_directories', []):
                    project_dir = ProjectDirectory(
                        name=dir_data['name'],
                        path=dir_data['path'],
                        description=dir_data.get('description', '')
                    )
                    self.project_directories.append(project_dir)
                
                # 加载提供商
                for provider_data in config_data.get('providers', []):
                    provider = ProviderConfig(
                        name=provider_data['name'],
                        type=ProviderType(provider_data['type']),
                        base_url=provider_data['base_url'],
                        api_key=provider_data['api_key'],
                        model=provider_data['model'],
                        small_fast_model=provider_data['small_fast_model'],
                        custom_headers=provider_data.get('custom_headers'),
                        priority=provider_data.get('priority', 1),
                        max_retries=provider_data.get('max_retries', 3),
                        timeout=provider_data.get('timeout', 30.0)
                    )
                    self.providers.append(provider)
                    self.health_status[provider.name] = HealthStatus(
                        provider_name=provider.name,
                        is_healthy=False,
                        response_time=float('inf'),
                        last_check=0
                    )
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            "providers": [
                {
                    "name": "openrouter",
                    "type": "openrouter",
                    "base_url": "https://cc.yovy.app",
                    "api_key": "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",
                    "model": "moonshotai/kimi-k2:free",
                    "small_fast_model": "moonshotai/kimi-k2:free",
                    "custom_headers": {"x-api-key": "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"},
                    "priority": 1
                },
                {
                    "name": "custom_anthropic",
                    "type": "custom_anthropic", 
                    "base_url": "https://api.jiuwanliguoxue.com/",
                    "api_key": "sk-acw-d97ae014-3f6dd2cd2af22cdf",
                    "model": "moonshotai/kimi-k2:free",
                    "small_fast_model": "moonshotai/kimi-k2:free",
                    "priority": 2
                },
                {
                    "name": "deepseek",
                    "type": "deepseek",
                    "base_url": "https://api.deepseek.com/v1",
                    "api_key": "YOUR_DEEPSEEK_API_KEY",
                    "model": "deepseek-chat",
                    "small_fast_model": "deepseek-chat",
                    "priority": 3
                },
                {
                    "name": "moonshot",
                    "type": "moonshot",
                    "base_url": "https://api.moonshot.cn/v1",
                    "api_key": "YOUR_MOONSHOT_API_KEY",
                    "model": "moonshot-v1-8k",
                    "small_fast_model": "moonshot-v1-8k",
                    "priority": 4
                }
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        print(f"默认配置文件已创建: {self.config_file}")
        self.load_config()
    
    def save_config(self):
        """保存配置到文件"""
        config_data = {
            "project_directories": [
                {
                    "name": proj_dir.name,
                    "path": proj_dir.path,
                    "description": proj_dir.description
                }
                for proj_dir in self.project_directories
            ],
            "providers": [
                {
                    "name": provider.name,
                    "type": provider.type.value,
                    "base_url": provider.base_url,
                    "api_key": provider.api_key,
                    "model": provider.model,
                    "small_fast_model": provider.small_fast_model,
                    "priority": provider.priority,
                    "max_retries": provider.max_retries,
                    "timeout": provider.timeout,
                    **({"custom_headers": provider.custom_headers} if provider.custom_headers else {})
                }
                for provider in self.providers
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    def add_project_directory(self, name: str, path: str, description: str = ""):
        """添加项目目录"""
        # 检查是否已存在
        for proj_dir in self.project_directories:
            if proj_dir.name == name or proj_dir.path == path:
                return False  # 已存在
        
        # 添加新项目目录
        new_proj_dir = ProjectDirectory(name=name, path=path, description=description)
        self.project_directories.append(new_proj_dir)
        self.save_config()
        return True
    
    async def check_provider_health(self, provider: ProviderConfig) -> HealthStatus:
        """检查单个提供者的健康状态"""
        start_time = time.time()
        
        try:
            headers = {
                "Content-Type": "application/json",
                **(provider.custom_headers or {})
            }
            
            if provider.type == ProviderType.OPENROUTER:
                headers["Authorization"] = f"Bearer {provider.api_key}"
                headers["HTTP-Referer"] = "https://claude.ai"
                # 使用简单的根路径检查，避免404
                test_url = f"{provider.base_url.rstrip('/')}"
            elif provider.type == ProviderType.CUSTOM_ANTHROPIC:
                headers["x-api-key"] = provider.api_key
                # 对于 custom_anthropic，检查根路径或v1端点
                test_url = f"{provider.base_url.rstrip('/')}"
            elif provider.type == ProviderType.DEEPSEEK:
                headers["Authorization"] = f"Bearer {provider.api_key}"
                test_url = f"{provider.base_url}/models"
            elif provider.type == ProviderType.MOONSHOT:
                headers["Authorization"] = f"Bearer {provider.api_key}"
                # Moonshot 使用根路径检查，避免 /models 404
                test_url = f"{provider.base_url.rstrip('/')}"
            elif provider.type == ProviderType.ZHIPU:
                headers["Authorization"] = f"Bearer {provider.api_key}"
                test_url = f"{provider.base_url}/models"
            elif provider.type == ProviderType.BAICHUAN:
                headers["Authorization"] = f"Bearer {provider.api_key}"
                test_url = f"{provider.base_url}/models"
            elif provider.type == ProviderType.OFFICIAL_ANTHROPIC:
                headers["x-api-key"] = provider.api_key
                test_url = "https://api.anthropic.com/v1/models"
            elif provider.type == ProviderType.AZURE_OPENAI:
                headers["api-key"] = provider.api_key
                test_url = f"{provider.base_url}/openai/deployments?api-version=2023-05-15"
            elif provider.type == ProviderType.GEMINI:
                test_url = f"{provider.base_url}/models?key={provider.api_key}"
            elif provider.type == ProviderType.LOCAL_OLLAMA:
                test_url = f"{provider.base_url}/api/tags"
            
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=provider.timeout)
            ) as session:
                async with session.get(test_url, headers=headers) as response:
                    response_time = time.time() - start_time
                    
                    # 更宽松的健康检查：200=成功，401/403=服务存在但权限问题，404=端点不存在但可能服务正常
                    if response.status in [200, 401, 403, 404]:
                        return HealthStatus(
                            provider_name=provider.name,
                            is_healthy=True,
                            response_time=response_time,
                            last_check=time.time()
                        )
                    else:
                        return HealthStatus(
                            provider_name=provider.name,
                            is_healthy=False,
                            response_time=response_time,
                            last_check=time.time(),
                            error_message=f"HTTP {response.status}"
                        )
        
        except Exception as e:
            return HealthStatus(
                provider_name=provider.name,
                is_healthy=False,
                response_time=time.time() - start_time,
                last_check=time.time(),
                error_message=str(e)
            )
    
    async def check_all_providers(self) -> Dict[str, HealthStatus]:
        """检查所有提供者的健康状态"""
        tasks = [self.check_provider_health(provider) for provider in self.providers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, HealthStatus):
                self.health_status[result.provider_name] = result
        
        return self.health_status
    
    def get_best_provider(self) -> Optional[str]:
        """获取最佳可用提供者"""
        healthy_providers = [
            name for name, status in self.health_status.items()
            if status.is_healthy
        ]
        
        if not healthy_providers:
            return None
        
        # 按优先级排序和响应时间排序
        provider_scores = []
        for name in healthy_providers:
            provider = next(p for p in self.providers if p.name == name)
            status = self.health_status[name]
            score = provider.priority / max(status.response_time, 0.1)
            provider_scores.append((name, score))
        
        provider_scores.sort(key=lambda x: x[1], reverse=True)
        return provider_scores[0][0] if provider_scores else None
    
    def activate_provider(self, provider_name: str) -> bool:
        """激活指定提供者"""
        provider = next((p for p in self.providers if p.name == provider_name), None)
        if not provider:
            print(f"未找到提供者: {provider_name}")
            return False
        
        # 清理所有相关的环境变量，避免混用
        anthropic_vars_to_clear = [
            "ANTHROPIC_API_KEY",
            "ANTHROPIC_AUTH_TOKEN", 
            "ANTHROPIC_MODEL",
            "ANTHROPIC_SMALL_FAST_MODEL",
            "ANTHROPIC_BASE_URL"
        ]
        
        for var in anthropic_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
        
        # 基础环境变量
        env_vars = {
            "ANTHROPIC_BASE_URL": provider.base_url,
        }
        
        # 根据提供商类型设置不同的环境变量
        # 根据提供商类型设置正确的环境变量
        if provider.type == ProviderType.OPENROUTER:
            # OpenRouter 使用 API_KEY 和明确的模型名称
            env_vars["ANTHROPIC_API_KEY"] = provider.api_key
            env_vars["ANTHROPIC_MODEL"] = provider.model
            env_vars["ANTHROPIC_SMALL_FAST_MODEL"] = provider.small_fast_model
        elif provider.type == ProviderType.CUSTOM_ANTHROPIC:
            # Claude兼容API使用 AUTH_TOKEN
            env_vars["ANTHROPIC_AUTH_TOKEN"] = provider.api_key
            # 只有在明确指定模型时才设置模型参数
            if provider.model and provider.model != "auto":
                env_vars["ANTHROPIC_MODEL"] = provider.model
                env_vars["ANTHROPIC_SMALL_FAST_MODEL"] = provider.small_fast_model
        elif provider.type == ProviderType.MOONSHOT:
            # Moonshot 兼容 Claude 格式，使用 API_KEY
            env_vars["ANTHROPIC_API_KEY"] = provider.api_key
            if provider.model and provider.model != "auto":
                env_vars["ANTHROPIC_MODEL"] = provider.model
                env_vars["ANTHROPIC_SMALL_FAST_MODEL"] = provider.small_fast_model
        else:
            # 其他提供商的标准配置，默认使用 API_KEY
            env_vars["ANTHROPIC_API_KEY"] = provider.api_key
            if provider.model and provider.model != "auto":
                env_vars["ANTHROPIC_MODEL"] = provider.model
                env_vars["ANTHROPIC_SMALL_FAST_MODEL"] = provider.small_fast_model
        
        # 自定义头部处理
        if provider.custom_headers:
            for key, value in provider.custom_headers.items():
                env_var_name = f"ANTHROPIC_CUSTOM_HEADERS_{key.replace('-', '_').upper()}"
                env_vars[env_var_name] = value
        
        # 更新环境变量
        for key, value in env_vars.items():
            os.environ[key] = value
        
        self.current_provider = provider_name
        
        # 创建激活文件
        activate_script = f"""#!/bin/bash
# Claude Code AI 提供者切换脚本 - {provider.name}
# 提供商类型: {provider.type.value}

"""
        
        # 添加环境变量到脚本
        for key, value in env_vars.items():
            activate_script += f'export {key}="{value}"\n'
        
        # 添加提供商特定说明
        if provider.name == "claude_code_nexus":
            activate_script += """
# Claude Nekro 特殊配置说明:
# - 使用 ANTHROPIC_AUTH_TOKEN 而不是 ANTHROPIC_API_KEY
# - 内置模型映射，无需指定模型名称
echo "已激活 Claude Nekro 提供商"
"""
        elif provider.name == "openrouter_yovy":
            activate_script += """
# OpenRouter 特殊配置说明:
# - 需要明确指定模型名称
# - 支持多种模型选择
echo "已激活 OpenRouter 提供商"
"""
        elif provider.type == ProviderType.MOONSHOT:
            activate_script += """
# Moonshot 特殊配置说明:
# - 兼容 Claude 格式
# - 模型名称可选
echo "已激活 Moonshot 提供商"
"""
        else:
            activate_script += f"""
echo "已激活 {provider.name} 提供商"
"""
        
        activate_script += 'echo "可以直接使用 claude 命令"\n'
        
        with open("activate_provider.sh", "w") as f:
            f.write(activate_script)
        
        print(f"已激活提供者: {provider_name}")
        print("运行以下命令应用更改:")
        print(f"source activate_provider.sh")
        
        return True
    
    def list_providers(self) -> None:
        """列出所有提供者状态"""
        print("\n=== 提供者状态 ===")
        for provider in self.providers:
            health = self.health_status.get(provider.name)
            if health:
                status = "✅ 正常" if health.is_healthy else "❌ 故障"
                response_time = f"{health.response_time:.2f}s" if health.response_time != float('inf') else "超时"
                print(f"{provider.name}: {status} (响应时间: {response_time})")
        
        if self.current_provider:
            print(f"\n当前激活: {self.current_provider}")
    
    def get_current_env(self) -> Dict[str, str]:
        """获取当前环境变量"""
        env_vars = {}
        for key in os.environ:
            if key.startswith("ANTHROPIC_"):
                env_vars[key] = os.environ[key]
        return env_vars


async def main():
    """主函数"""
    switcher = AIProviderSwitcher()
    
    # 检查所有提供者状态
    print("正在检测提供者健康状态...")
    await switcher.check_all_providers()
    
    # 显示状态
    switcher.list_providers()
    
    # 选择最佳提供者
    best_provider = switcher.get_best_provider()
    if best_provider:
        print(f"\n推荐切换到: {best_provider}")
        response = input("是否切换到推荐提供者？(y/n): ")
        if response.lower() in ['y', 'yes', '是']:
            switcher.activate_provider(best_provider)
    else:
        print("\n❌ 所有提供者都不可用")


if __name__ == "__main__":
    asyncio.run(main())