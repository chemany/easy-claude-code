#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easy Claude Code - Terminal Launcher

Cross-platform terminal launcher with automatic environment setup for Claude Code.
Supports multiple desktop environments and terminal emulators.

Repository: https://github.com/username/easy-claude-code
License: MIT
"""

import os
import subprocess
import shutil
import tempfile

def detect_available_terminals():
    """检测系统中可用的终端"""
    terminals = [
        # Ubuntu/Debian 系统通用终端
        ('x-terminal-emulator', ['x-terminal-emulator', '-e']),  # Debian/Ubuntu 系统默认终端
        ('sensible-terminal', ['sensible-terminal', '-e']),      # Debian/Ubuntu 系统智能终端选择器
        
        # GNOME 桌面环境 (Ubuntu 默认)
        ('gnome-terminal', ['gnome-terminal', '--']),
        ('gnome-terminal-server', ['gnome-terminal', '--']),     # 新版本的gnome-terminal
        
        # XFCE 桌面环境  
        ('xfce4-terminal', ['xfce4-terminal', '--hold', '-e']),
        
        # KDE 桌面环境
        ('konsole', ['konsole', '-e']),
        
        # MATE 桌面环境 (Ubuntu MATE)
        ('mate-terminal', ['mate-terminal', '-e']),
        
        # 现代终端应用
        ('tilix', ['tilix', '-e']),                             # Ubuntu 官方仓库中的现代终端
        ('terminator', ['terminator', '-e']),                   # 流行的多窗格终端
        ('alacritty', ['alacritty', '-e']),                     # GPU 加速终端
        ('kitty', ['kitty']),                                   # 现代终端模拟器
        
        # 轻量级终端
        ('lxterminal', ['lxterminal', '-e']),                   # LXDE 终端
        ('xterm', ['xterm', '-hold', '-e']),                    # 经典终端
        ('urxvt', ['urxvt', '-hold', '-e']),                    # rxvt-unicode
        ('rxvt', ['rxvt', '-hold', '-e']),                      # rxvt
        ('sakura', ['sakura', '-e']),                           # 轻量级终端
        ('qterminal', ['qterminal', '-e']),                     # LXQt 终端
        
        # 其他终端
        ('deepin-terminal', ['deepin-terminal', '-e']),         # Deepin 终端
        ('terminology', ['terminology', '-e']),                 # Enlightenment 终端
        ('st', ['st', '-e']),                                   # Simple Terminal
    ]
    
    available = []
    for name, cmd in terminals:
        if shutil.which(name):
            available.append((name, cmd))
    
    return available

def get_desktop_environment():
    """检测当前桌面环境"""
    desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
    session = os.environ.get('DESKTOP_SESSION', '').lower()
    gdm_session = os.environ.get('GDMSESSION', '').lower()
    
    # Ubuntu 及其变体
    if 'ubuntu' in desktop or 'ubuntu' in session:
        if 'gnome' in desktop or 'gnome' in session:
            return 'ubuntu-gnome'
        elif 'unity' in desktop or 'unity' in session:
            return 'ubuntu-unity'
        else:
            return 'ubuntu'
    elif 'gnome' in desktop or 'unity' in desktop or 'gnome' in session or 'unity' in session:
        return 'gnome'
    elif 'xfce' in desktop or 'xfce' in session or 'xfce' in gdm_session:
        return 'xfce'
    elif 'kde' in desktop or 'plasma' in desktop or 'kde' in session:
        return 'kde'
    elif 'mate' in desktop or 'mate' in session:
        return 'mate'
    elif 'lxde' in desktop or 'lxde' in session:
        return 'lxde'
    elif 'lxqt' in desktop or 'lxqt' in session:
        return 'lxqt'
    elif 'deepin' in desktop or 'deepin' in session:
        return 'deepin'
    elif 'cinnamon' in desktop or 'cinnamon' in session:
        return 'cinnamon'
    elif 'pantheon' in desktop or 'pantheon' in session:
        return 'pantheon'  # Elementary OS
    else:
        return 'unknown'

def launch_terminal(command, env=None, working_dir=None, auto_claude=False):
    """
    启动终端并执行命令
    
    Args:
        command (str): 要执行的命令
        env (dict): 环境变量
        working_dir (str): 工作目录
        auto_claude (bool): 是否自动启动claude命令
    
    Returns:
        tuple: (success, terminal_name, error_message)
    """
    available_terminals = detect_available_terminals()
    
    if not available_terminals:
        return False, None, "未找到任何可用的终端应用"
    
    desktop_env = get_desktop_environment()
    
    # 根据桌面环境排序终端优先级
    priority_order = {
        # Ubuntu 及其变体 - 优先使用系统默认的通用终端
        'ubuntu': ['x-terminal-emulator', 'sensible-terminal', 'gnome-terminal', 'tilix', 'terminator', 'xterm'],
        'ubuntu-gnome': ['gnome-terminal', 'x-terminal-emulator', 'tilix', 'terminator', 'xterm'],
        'ubuntu-unity': ['gnome-terminal', 'x-terminal-emulator', 'unity-terminal', 'xterm'],
        
        # 标准桌面环境
        'gnome': ['gnome-terminal', 'gnome-terminal-server', 'tilix', 'terminator', 'xterm'],
        'xfce': ['xfce4-terminal', 'x-terminal-emulator', 'xterm', 'lxterminal'],
        'kde': ['konsole', 'x-terminal-emulator', 'xterm'],
        'mate': ['mate-terminal', 'x-terminal-emulator', 'xterm'],
        'lxde': ['lxterminal', 'x-terminal-emulator', 'xterm'],
        'lxqt': ['qterminal', 'x-terminal-emulator', 'lxterminal', 'xterm'],
        'deepin': ['deepin-terminal', 'x-terminal-emulator', 'xterm'],
        'cinnamon': ['gnome-terminal', 'x-terminal-emulator', 'tilix', 'xterm'],
        'pantheon': ['io.elementary.terminal', 'gnome-terminal', 'x-terminal-emulator', 'xterm'],
        
        # 通用回退选项
        'unknown': ['x-terminal-emulator', 'sensible-terminal', 'gnome-terminal', 'xfce4-terminal', 'konsole', 'xterm'],
    }
    
    # 重新排序可用终端
    preferred_terminals = priority_order.get(desktop_env, [])
    sorted_terminals = []
    
    # 首先添加首选终端
    for pref in preferred_terminals:
        for name, cmd in available_terminals:
            if name == pref:
                sorted_terminals.append((name, cmd))
                break
    
    # 然后添加其他可用终端
    for name, cmd in available_terminals:
        if not any(name == t[0] for t in sorted_terminals):
            sorted_terminals.append((name, cmd))
    
    # 准备环境变量
    if env is None:
        env = os.environ.copy()
    else:
        full_env = os.environ.copy()
        full_env.update(env)
        env = full_env
    
    # 准备启动命令 - 将环境变量内联到命令中
    env_setup = ""
    if env:
        for key, value in env.items():
            if key.startswith("ANTHROPIC_"):
                # 转义引号以防止shell问题
                escaped_value = value.replace('"', '\\"')
                env_setup += f'export {key}="{escaped_value}"; '
    
    # 根据是否自动化添加不同的设置命令
    if auto_claude:
        setup_cmd = f"""
clear
echo "🚀 正在启动 Claude Code..."
echo "==============================================="
sleep 1

# 首先加载用户shell配置确保PATH正确
source ~/.bashrc 2>/dev/null || source ~/.profile 2>/dev/null || true

# 确保NVM和Node环境可用
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

echo "📦 环境配置完成!"
echo "当前环境变量:"
env | grep ANTHROPIC_ | head -5
echo
echo "📁 工作目录: $(pwd)"
echo
sleep 1

echo "🔍 检查Claude命令..."
if command -v claude &> /dev/null; then
    echo "✅ 找到Claude命令: $(which claude)"
    echo
    echo "🎉 正在自动启动Claude Code..."
    echo "==============================================="
    sleep 1
    
    # 自动执行claude命令
    claude || (echo "❌ Claude启动失败" && sleep 3)
    
    echo
    echo "✅ Claude执行完成"
    echo "💡 环境变量仍然有效，可以再次运行claude"
    echo "💡 或者执行其他开发任务"
else
    echo "⚠️  未找到Claude命令"
    echo "🔧 尝试手动加载NVM环境..."
    nvm use default 2>/dev/null && echo "✅ NVM环境已加载" || echo "⚠️  NVM加载失败"
    
    if command -v claude &> /dev/null; then
        echo "✅ 现在找到Claude命令了: $(which claude)"
        echo "🎉 正在启动Claude Code..."
        claude || (echo "❌ Claude启动失败" && sleep 3)
    else
        echo "💡 环境变量已设置，可以手动运行 claude 命令"
        echo "💡 或者检查Claude Code是否正确安装"
    fi
fi

echo
echo "🎯 终端保持打开状态，可以继续工作..."
echo

# 启动交互式bash，在claude执行后保持终端可用
exec bash
"""
    else:
        setup_cmd = """
# 加载用户的shell配置
source ~/.bashrc 2>/dev/null || source ~/.profile 2>/dev/null || true

# 确保NVM和Claude可用
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion"

echo "🎉 Claude Code 环境已就绪!"
echo "当前环境变量:"
env | grep ANTHROPIC_ | head -5
echo
echo "Claude 命令位置:"
which claude 2>/dev/null || echo "⚠️  Claude命令未找到，请检查安装"
echo
echo "可以直接使用 claude 命令"
echo
"""
    
    if working_dir:
        if auto_claude:
            full_command = f'{env_setup}cd "{working_dir}"; {setup_cmd}'
        elif command:
            full_command = f'{env_setup}cd "{working_dir}"; {setup_cmd}{command}; bash'
        else:
            full_command = f'{env_setup}cd "{working_dir}"; {setup_cmd}bash'
    else:
        if auto_claude:
            full_command = f'{env_setup}{setup_cmd}'
        elif command:
            full_command = f'{env_setup}{setup_cmd}{command}; bash'
        else:
            full_command = f'{env_setup}{setup_cmd}bash'
    
    # 尝试启动终端
    for terminal_name, terminal_cmd in sorted_terminals:
        try:
            if terminal_name == 'gnome-terminal':
                # GNOME Terminal 特殊处理
                cmd = terminal_cmd + ['bash', '-c', full_command]
            elif terminal_name == 'konsole':
                # KDE Konsole 特殊处理
                cmd = terminal_cmd + ['bash', '-c', full_command]
            elif terminal_name == 'xfce4-terminal':
                # XFCE Terminal 特殊处理 - 使用临时脚本文件
                with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as temp_script:
                    temp_script.write(f"#!/bin/bash\n{full_command}")
                    temp_script_path = temp_script.name
                
                os.chmod(temp_script_path, 0o755)
                cmd = ['xfce4-terminal', '-e', temp_script_path]
                
                # 延迟删除脚本文件
                import threading
                def cleanup_later():
                    import time
                    time.sleep(10)  # 给终端时间读取脚本
                    try:
                        os.unlink(temp_script_path)
                    except:
                        pass
                threading.Thread(target=cleanup_later, daemon=True).start()
            elif terminal_name == 'kitty':
                # Kitty 特殊处理
                cmd = terminal_cmd + ['bash', '-c', full_command]
            else:
                # 其他终端的通用处理
                cmd = terminal_cmd + ['bash', '-c', full_command]
            
            # 启动终端
            subprocess.Popen(cmd, env=env, cwd=working_dir or os.getcwd())
            return True, terminal_name, None
            
        except Exception as e:
            continue
    
    return False, None, f"所有终端启动失败: {str(e)}"

def test_terminal_detection():
    """测试终端检测功能"""
    print("🔍 检测系统终端...")
    
    desktop_env = get_desktop_environment()
    print(f"桌面环境: {desktop_env.upper()}")
    
    available_terminals = detect_available_terminals()
    print(f"\n📋 可用终端 ({len(available_terminals)} 个):")
    
    for name, cmd in available_terminals:
        print(f"  ✅ {name:<15} - {' '.join(cmd[:3])}...")
    
    if not available_terminals:
        print("  ❌ 未找到任何终端")
        return False
    
    # 测试启动
    print(f"\n🚀 测试启动终端...")
    success, terminal_name, error = launch_terminal(
        'echo "终端测试成功!" && echo "按回车键继续..." && read',
        env={'TEST_VAR': 'Hello World'},
        working_dir=os.getcwd()
    )
    
    if success:
        print(f"✅ 成功启动: {terminal_name}")
    else:
        print(f"❌ 启动失败: {error}")
    
    return success

if __name__ == "__main__":
    test_terminal_detection()