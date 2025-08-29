#!/usr/bin/env python3
"""
Easy Claude Code - AI Provider Switcher
Easily switch between different AI providers for Claude Code with a beautiful GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import asyncio
import os
import threading
import json
from provider_switch import AIProviderSwitcher, ProviderType
from terminal_launcher import launch_terminal

class ProviderEditDialog:
    """提供商编辑对话框"""
    
    def __init__(self, parent, title, provider=None):
        self.parent = parent
        self.provider = provider  # 如果是编辑模式，传入现有provider
        self.result = False
        self.data = {}
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x700")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.center_window()
        
        # 创建界面
        self.create_widgets()
        
        # 如果是编辑模式，填入现有数据
        if self.provider:
            self.load_provider_data()
    
    def center_window(self):
        """居中显示对话框"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"600x700+{x}+{y}")
    
    def create_widgets(self):
        """创建对话框组件"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 滚动容器
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 基本信息
        basic_frame = ttk.LabelFrame(scrollable_frame, text="基本信息", padding="10")
        basic_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 提供商名称
        ttk.Label(basic_frame, text="名称*:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(basic_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 如果是编辑模式，禁用名称修改
        if self.provider:
            name_entry.config(state='disabled')
        
        # 提供商类型
        ttk.Label(basic_frame, text="类型*:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar()
        type_combo = ttk.Combobox(basic_frame, textvariable=self.type_var, width=37, state="readonly")
        type_combo['values'] = [ptype.value for ptype in ProviderType]
        type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # API配置
        api_frame = ttk.LabelFrame(scrollable_frame, text="API配置", padding="10")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Base URL
        ttk.Label(api_frame, text="Base URL*:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.base_url_var = tk.StringVar()
        ttk.Entry(api_frame, textvariable=self.base_url_var, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # API Key
        ttk.Label(api_frame, text="API Key*:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar()
        ttk.Entry(api_frame, textvariable=self.api_key_var, width=40, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 模型配置
        model_frame = ttk.LabelFrame(scrollable_frame, text="模型配置", padding="10")
        model_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 主模型
        ttk.Label(model_frame, text="主模型*:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar()
        ttk.Entry(model_frame, textvariable=self.model_var, width=40).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 快速模型
        ttk.Label(model_frame, text="快速模型*:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.small_fast_model_var = tk.StringVar()
        ttk.Entry(model_frame, textvariable=self.small_fast_model_var, width=40).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 高级配置
        advanced_frame = ttk.LabelFrame(scrollable_frame, text="高级配置", padding="10")
        advanced_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 优先级
        ttk.Label(advanced_frame, text="优先级:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.IntVar(value=1)
        ttk.Spinbox(advanced_frame, from_=1, to=10, textvariable=self.priority_var, width=38).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 最大重试次数
        ttk.Label(advanced_frame, text="最大重试:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_retries_var = tk.IntVar(value=3)
        ttk.Spinbox(advanced_frame, from_=1, to=10, textvariable=self.max_retries_var, width=38).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 超时时间
        ttk.Label(advanced_frame, text="超时时间(秒):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.timeout_var = tk.DoubleVar(value=30.0)
        ttk.Spinbox(advanced_frame, from_=5.0, to=120.0, increment=5.0, textvariable=self.timeout_var, width=38).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # 自定义头部
        headers_frame = ttk.LabelFrame(scrollable_frame, text="自定义HTTP头部 (JSON格式)", padding="10")
        headers_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.custom_headers_text = tk.Text(headers_frame, height=4, width=60, font=('Consolas', 9))
        self.custom_headers_text.pack(fill=tk.BOTH, expand=True)
        
        # 按钮
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="确定", command=self.on_ok).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="取消", command=self.on_cancel).pack(side=tk.RIGHT)
        
        # 配置网格权重
        basic_frame.columnconfigure(1, weight=1)
        api_frame.columnconfigure(1, weight=1)
        model_frame.columnconfigure(1, weight=1)
        advanced_frame.columnconfigure(1, weight=1)
        
        # 打包滚动组件
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_provider_data(self):
        """加载提供商数据到表单"""
        if not self.provider:
            return
        
        self.name_var.set(self.provider.name)
        self.type_var.set(self.provider.type.value)
        self.base_url_var.set(self.provider.base_url)
        self.api_key_var.set(self.provider.api_key)
        self.model_var.set(self.provider.model)
        self.small_fast_model_var.set(self.provider.small_fast_model)
        self.priority_var.set(self.provider.priority)
        self.max_retries_var.set(self.provider.max_retries)
        self.timeout_var.set(self.provider.timeout)
        
        if self.provider.custom_headers:
            self.custom_headers_text.insert(tk.END, json.dumps(self.provider.custom_headers, indent=2, ensure_ascii=False))
    
    def validate_data(self):
        """验证表单数据"""
        errors = []
        
        if not self.name_var.get().strip():
            errors.append("名称不能为空")
        
        if not self.type_var.get():
            errors.append("请选择提供商类型")
        
        if not self.base_url_var.get().strip():
            errors.append("Base URL不能为空")
        
        if not self.api_key_var.get().strip():
            errors.append("API Key不能为空")
        
        if not self.model_var.get().strip():
            errors.append("主模型不能为空")
        
        if not self.small_fast_model_var.get().strip():
            errors.append("快速模型不能为空")
        
        # 验证自定义头部JSON
        headers_text = self.custom_headers_text.get(1.0, tk.END).strip()
        custom_headers = None
        if headers_text:
            try:
                custom_headers = json.loads(headers_text)
                if not isinstance(custom_headers, dict):
                    errors.append("自定义头部必须是JSON对象格式")
            except json.JSONDecodeError as e:
                errors.append(f"自定义头部JSON格式错误: {e}")
        
        if errors:
            messagebox.showerror("验证错误", "\n".join(errors))
            return False
        
        # 保存数据
        self.data = {
            'name': self.name_var.get().strip(),
            'provider_type': self.type_var.get(),
            'base_url': self.base_url_var.get().strip(),
            'api_key': self.api_key_var.get().strip(),
            'model': self.model_var.get().strip(),
            'small_fast_model': self.small_fast_model_var.get().strip(),
            'custom_headers': custom_headers,
            'priority': self.priority_var.get(),
            'max_retries': self.max_retries_var.get(),
            'timeout': self.timeout_var.get()
        }
        
        return True
    
    def on_ok(self):
        """确定按钮回调"""
        if self.validate_data():
            self.result = True
            self.dialog.destroy()
    
    def on_cancel(self):
        """取消按钮回调"""
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """显示对话框并返回结果"""
        self.dialog.wait_window()
        return self.result
    
    def get_data(self):
        """获取表单数据"""
        return self.data

class AIProviderGUI_V2:
    def __init__(self, config_file="providers.json"):
        self.root = tk.Tk()
        self.root.title("Easy Claude Code - AI Provider Switcher")
        self.root.geometry("1400x800")
        
        # 设置样式
        self.setup_theme()
        
        self.switcher = AIProviderSwitcher(config_file)
        
        # 创建主界面
        self.create_widgets()
        
        # 加载配置并刷新显示
        self.update_provider_list()
        self.refresh_projects()
        
        # 启动时自动检查提供商健康状态
        self.root.after(100, self.check_providers_health)
    
    def setup_theme(self):
        """设置主题样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置颜色
        style.configure('Healthy.TLabel', foreground='green')
        style.configure('Unhealthy.TLabel', foreground='red') 
        style.configure('Active.TLabel', foreground='blue', font=('TkDefaultFont', 9, 'bold'))
        style.configure('Title.TLabel', font=('TkDefaultFont', 14, 'bold'))
        style.configure('Section.TLabel', font=('TkDefaultFont', 11, 'bold'))
    
    def create_widgets(self):
        """创建主界面组件 - 左右分栏布局"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="Easy Claude Code", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        
        # 左侧面板 - AI Provider 管理
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 右侧面板 - 项目目录和终端操作
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 创建左侧内容
        self.create_provider_section(left_panel)
        
        # 创建右侧内容
        self.create_project_and_terminal_section(right_panel)
        
        # 配置网格权重 - 调整左右比例使其更对称
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # 左侧占1份
        main_frame.columnconfigure(1, weight=1)  # 右侧占1份，实现对称
        main_frame.rowconfigure(1, weight=1)
    
    def create_provider_section(self, parent):
        """创建AI Provider管理区域"""
        # 提供商列表
        provider_frame = ttk.LabelFrame(parent, text="🤖 AI Provider 管理", padding="10")
        provider_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 创建Treeview
        columns = ('name', 'type', 'model', 'status', 'response_time', 'priority')
        self.provider_tree = ttk.Treeview(provider_frame, columns=columns, show='tree headings', height=10)
        
        # 配置列
        self.provider_tree.heading('#0', text='')
        self.provider_tree.column('#0', width=30)
        
        self.provider_tree.heading('name', text='提供商名称')
        self.provider_tree.column('name', width=150)
        
        self.provider_tree.heading('type', text='类型')
        self.provider_tree.column('type', width=120)
        
        self.provider_tree.heading('model', text='模型')
        self.provider_tree.column('model', width=150)
        
        self.provider_tree.heading('status', text='状态')
        self.provider_tree.column('status', width=80)
        
        self.provider_tree.heading('response_time', text='响应时间')
        self.provider_tree.column('response_time', width=80)
        
        self.provider_tree.heading('priority', text='优先级')
        self.provider_tree.column('priority', width=60)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(provider_frame, orient="vertical", command=self.provider_tree.yview)
        self.provider_tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局
        self.provider_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 控制按钮
        button_frame = ttk.Frame(provider_frame)
        button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        buttons = [
            ("刷新状态", self.check_providers_health, "info"),
            ("激活选中", self.activate_selected, "info"),
            ("添加提供商", self.add_provider, "secondary"),
            ("编辑配置", self.edit_provider, "secondary"),
            ("删除提供商", self.delete_provider, "danger"),
        ]
        
        for i, (text, command, style) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.grid(row=i//3, column=i%3, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # 配置权重
        provider_frame.columnconfigure(0, weight=1)
        provider_frame.rowconfigure(0, weight=1)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)
    
    def create_project_and_terminal_section(self, parent):
        """创建项目目录和终端操作区域"""
        # 项目目录区域 - 减少padding
        project_frame = ttk.LabelFrame(parent, text="📁 项目目录", padding="8")
        project_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N), pady=(0, 5))
        
        # 项目选择
        project_select_frame = ttk.Frame(project_frame)
        project_select_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(project_select_frame, text="选择项目:").grid(row=0, column=0, sticky=tk.W)
        
        self.project_var = tk.StringVar(value="当前目录")
        self.project_combo = ttk.Combobox(project_select_frame, textvariable=self.project_var, width=30, state="readonly")
        self.project_combo.grid(row=0, column=1, padx=(10, 5), sticky=(tk.W, tk.E))
        
        # 添加文件夹选择按钮
        browse_btn = ttk.Button(project_select_frame, text="📂 浏览", command=self.browse_folder)
        browse_btn.grid(row=0, column=2, padx=5)
        
        refresh_btn = ttk.Button(project_select_frame, text="🔄", command=self.refresh_projects)
        refresh_btn.grid(row=0, column=3, padx=5)
        
        # 显示选中的路径
        self.project_path_label = ttk.Label(project_frame, text="", foreground="gray")
        self.project_path_label.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 绑定项目选择变化事件
        self.project_combo.bind('<<ComboboxSelected>>', self.on_project_changed)
        
        # 状态显示区域 - 移到右侧中间位置，减少padding和间距
        status_frame = ttk.LabelFrame(parent, text="📊 当前状态", padding="8")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), pady=(3, 5))
        
        self.current_provider_label = ttk.Label(status_frame, text="当前激活: 未激活", style='Active.TLabel')
        self.current_provider_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 环境变量显示 - 减少高度
        self.env_display = tk.Text(status_frame, height=3, width=40, font=('Consolas', 9))
        self.env_display.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(3, 0))
        
        # 终端操作区域 - 减少padding和间距
        terminal_frame = ttk.LabelFrame(parent, text="🚀 终端操作", padding="8")
        terminal_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N), pady=(3, 0))
        
        # 终端命令设置 - 减少间距
        cmd_frame = ttk.Frame(terminal_frame)
        cmd_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(cmd_frame, text="终端命令:").grid(row=0, column=0, sticky=tk.W)
        self.terminal_command = tk.StringVar(value="claude")
        command_entry = ttk.Entry(cmd_frame, textvariable=self.terminal_command, width=30)
        command_entry.grid(row=0, column=1, padx=(10, 5), sticky=(tk.W, tk.E))
        
        # 选项设置 - 减少间距
        options_frame = ttk.Frame(terminal_frame)
        options_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        self.auto_apply_env = tk.BooleanVar(value=True)
        auto_check = ttk.Checkbutton(options_frame, text="自动应用环境变量", variable=self.auto_apply_env)
        auto_check.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.full_auto_mode = tk.BooleanVar(value=True)
        full_auto_check = ttk.Checkbutton(options_frame, text="完全自动化(直接可用claude)", variable=self.full_auto_mode)
        full_auto_check.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # 启动按钮
        launch_btn = ttk.Button(terminal_frame, text="🚀 一键启动", command=self.launch_terminal)
        launch_btn.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        # 配置权重
        project_select_frame.columnconfigure(1, weight=1)
        project_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(0, weight=1)
        cmd_frame.columnconfigure(1, weight=1)
        terminal_frame.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=0)  # 项目目录固定高度
        parent.rowconfigure(1, weight=1)  # 状态区域可扩展
        parent.rowconfigure(2, weight=0)  # 终端操作固定高度
    
    def browse_folder(self):
        """浏览选择文件夹"""
        folder_path = filedialog.askdirectory(
            title="选择项目文件夹",
            initialdir=os.getcwd()
        )
        
        if folder_path:
            # 添加到项目列表
            folder_name = os.path.basename(folder_path)
            
            # 使用文件夹名作为项目名，避免冲突的显示名
            project_name = folder_name
            
            # 尝试添加到配置文件
            success = self.switcher.add_project_directory(
                name=project_name,
                path=folder_path,
                description=f"Custom project directory - {folder_name}"
            )
            
            if success:
                # 刷新项目列表以显示新添加的项目
                self.refresh_projects()
                
                # 选择新添加的项目
                for display_name, path in self.project_paths.items():
                    if path == folder_path:
                        self.project_var.set(display_name)
                        self.on_project_changed(None)
                        break
                
                messagebox.showinfo("成功", f"已添加项目文件夹:\n{folder_path}\n\n项目已保存到配置文件中。")
            else:
                messagebox.showwarning("提示", f"项目文件夹已存在或添加失败:\n{folder_path}")
    
    def on_project_changed(self, event):
        """项目选择变化时的回调"""
        selected = self.project_var.get()
        if hasattr(self, 'project_paths') and selected in self.project_paths:
            path = self.project_paths[selected]
            self.project_path_label.config(text=f"路径: {path}")
        elif selected == "当前目录":
            self.project_path_label.config(text=f"路径: {os.getcwd()}")
        else:
            self.project_path_label.config(text="")
    
    def refresh_projects(self):
        """刷新项目列表"""
        project_names = ["当前目录"]
        self.project_paths = {"当前目录": os.getcwd()}
        
        # 从配置中加载项目目录
        for proj_dir in self.switcher.project_directories:
            display_name = f"{proj_dir.name} - {proj_dir.description}" if proj_dir.description else proj_dir.name
            project_names.append(display_name)
            self.project_paths[display_name] = proj_dir.path
        
        self.project_combo['values'] = project_names
        
        # 触发路径显示更新
        self.on_project_changed(None)
    
    def launch_terminal(self):
        """一键启动：自动激活选中提供商并启动终端"""
        command = self.terminal_command.get().strip()
        if not command:
            command = "claude"
        
        # 获取选择的项目目录
        project_dir = None
        selected_project = self.project_var.get()
        if selected_project in self.project_paths:
            project_path = self.project_paths[selected_project]
            if os.path.exists(project_path):
                project_dir = project_path
        
        try:
            # 自动激活选中的提供商（一键启动的核心逻辑）
            if self.auto_apply_env.get():
                # 获取选中的提供商
                selection = self.provider_tree.selection()
                if not selection:
                    messagebox.showwarning("提示", "请先选择一个提供商")
                    return
                
                item = self.provider_tree.item(selection[0])
                selected_provider = item['values'][0]
                
                # 自动激活选中的提供商
                print(f"🔄 自动激活提供商: {selected_provider}")
                if not self.switcher.activate_provider(selected_provider):
                    messagebox.showerror("错误", f"激活提供商 {selected_provider} 失败")
                    return
                
                # 更新界面显示
                self.update_provider_list()
                self.update_env_display()
                
                print(f"✅ 提供商 {selected_provider} 已自动激活")
                
                # 直接使用系统环境变量
                env = os.environ.copy()
                
                # 获取当前提供商配置（用于自定义头部处理）
                provider = next((p for p in self.switcher.providers if p.name == self.switcher.current_provider), None)
                if provider and provider.custom_headers:
                    for key, value in provider.custom_headers.items():
                        env_var_name = f"ANTHROPIC_CUSTOM_HEADERS_{key.replace('-', '_').upper()}"
                        env[env_var_name] = value
                
                # 检查是否启用完全自动化
                if self.full_auto_mode.get():
                    # 完全自动化模式：直接启动claude
                    success, terminal_name, error = launch_terminal(
                        command=None,
                        env=env,
                        working_dir=project_dir,
                        auto_claude=True
                    )
                else:
                    # 准备启动命令
                    welcome_msg = f'''echo "🎉 Claude Code 环境已就绪"
echo "当前提供商: {selected_provider}"
echo "可以直接使用 {command} 命令"
echo'''
                    
                    # 使用新的终端启动器
                    success, terminal_name, error = launch_terminal(
                        welcome_msg,
                        env=env,
                        working_dir=project_dir
                    )
                
                if success:
                    if self.full_auto_mode.get():
                        info_msg = f"🎉 一键启动成功!\n📱 终端: {terminal_name}\n🔄 已自动激活: {selected_provider}\n🚀 Claude命令将自动执行\n💡 执行完成后终端保持打开以便继续工作"
                    else:
                        info_msg = f"🎉 一键启动成功!\n📱 终端: {terminal_name}\n🔄 已自动激活: {selected_provider}\n📝 命令: {command}"
                    
                    if project_dir:
                        info_msg += f"\n📁 项目目录: {project_dir}"
                    messagebox.showinfo("启动成功", info_msg)
                else:
                    messagebox.showerror("错误", f"终端启动失败: {error}")
                    return
            else:
                # 普通启动
                launch_cmd = f'echo "终端已启动"\necho "可以使用 {command} 命令"'
                
                success, terminal_name, error = launch_terminal(
                    launch_cmd,
                    working_dir=project_dir
                )
                
                if success:
                    info_msg = f"已启动终端: {terminal_name}\n命令: {command}"
                    if project_dir:
                        info_msg += f"\n项目目录: {project_dir}"
                    messagebox.showinfo("成功", info_msg)
                else:
                    messagebox.showerror("错误", f"终端启动失败: {error}")
                    return
        
        except Exception as e:
            messagebox.showerror("错误", f"启动终端失败: {str(e)}")
    
    def update_provider_list(self):
        """更新提供商列表显示"""
        # 清空现有项目
        for item in self.provider_tree.get_children():
            self.provider_tree.delete(item)
        
        # 添加提供商
        for provider in self.switcher.providers:
            health = self.switcher.health_status.get(provider.name)
            
            if health:
                status = "✅正常" if health.is_healthy else "❌故障"
                response_time = f"{health.response_time:.2f}s" if health.response_time != float('inf') else "超时"
            else:
                status = "未检测"
                response_time = "N/A"
            
            # 标记当前激活的提供商
            icon = "🔹" if provider.name == self.switcher.current_provider else ""
            
            self.provider_tree.insert('', 'end', text=icon, values=(
                provider.name,
                provider.type.value,
                provider.model,
                status,
                response_time,
                provider.priority
            ))
        
        # 更新当前状态
        current = self.switcher.current_provider or "未激活"
        self.current_provider_label.config(text=f"当前激活: {current}")
        
        # 更新环境变量显示
        self.update_env_display()
    
    def update_env_display(self):
        """更新环境变量显示"""
        self.env_display.delete(1.0, tk.END)
        
        env_vars = {}
        for key, value in os.environ.items():
            if key.startswith("ANTHROPIC_"):
                env_vars[key] = value
        
        if env_vars:
            for key, value in sorted(env_vars.items()):
                self.env_display.insert(tk.END, f"{key}={value}\n")
        else:
            self.env_display.insert(tk.END, "当前未设置ANTHROPIC相关环境变量")
    
    def check_providers_health(self):
        """异步检查提供商健康状态"""
        def run_health_check():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.switcher.check_all_providers())
                # 在主线程中更新UI
                self.root.after(0, self.update_provider_list)
            finally:
                loop.close()
        
        # 在后台线程中运行
        threading.Thread(target=run_health_check, daemon=True).start()
    
    def activate_selected(self):
        """激活选中的提供商"""
        selection = self.provider_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个提供商")
            return
        
        item = self.provider_tree.item(selection[0])
        provider_name = item['values'][0]
        
        if self.switcher.activate_provider(provider_name):
            messagebox.showinfo("成功", f"已激活提供商: {provider_name}")
            self.update_provider_list()
        else:
            messagebox.showerror("错误", f"激活提供商失败: {provider_name}")
    
    def add_provider(self):
        """添加新提供商"""
        dialog = ProviderEditDialog(self.root, "添加提供商")
        if dialog.show():
            data = dialog.get_data()
            success = self.switcher.add_provider(**data)
            if success:
                messagebox.showinfo("成功", f"已添加提供商: {data['name']}")
                self.update_provider_list()
            else:
                messagebox.showerror("错误", "添加提供商失败 - 提供商名称可能已存在")
    
    def edit_provider(self):
        """编辑提供商"""
        selection = self.provider_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个提供商")
            return
        
        item = self.provider_tree.item(selection[0])
        provider_name = item['values'][0]
        
        # 获取当前提供商数据
        provider = next((p for p in self.switcher.providers if p.name == provider_name), None)
        if not provider:
            messagebox.showerror("错误", "找不到选中的提供商")
            return
        
        dialog = ProviderEditDialog(self.root, "编辑提供商", provider)
        if dialog.show():
            data = dialog.get_data()
            # 从数据中移除name，因为不能修改名称
            updates = {k: v for k, v in data.items() if k != 'name'}
            success = self.switcher.update_provider(provider_name, **updates)
            if success:
                messagebox.showinfo("成功", f"已更新提供商: {provider_name}")
                self.update_provider_list()
            else:
                messagebox.showerror("错误", "更新提供商失败")
    
    def delete_provider(self):
        """删除提供商"""
        selection = self.provider_tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个提供商")
            return
        
        item = self.provider_tree.item(selection[0])
        provider_name = item['values'][0]
        
        # 确认删除
        if messagebox.askyesno("确认删除", f"确定要删除提供商 '{provider_name}' 吗？\n\n这将永久删除该配置。"):
            success = self.switcher.delete_provider(provider_name)
            if success:
                messagebox.showinfo("成功", f"已删除提供商: {provider_name}")
                self.update_provider_list()
            else:
                messagebox.showerror("错误", "删除提供商失败")
    
    def run(self):
        """运行GUI"""
        self.root.mainloop()

def main():
    """主函数"""
    app = AIProviderGUI_V2()
    app.run()

if __name__ == "__main__":
    main()