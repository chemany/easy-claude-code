#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Easy Claude Code - Quick Launch Script

Simple entry point for launching the Easy Claude Code GUI application.
This script handles initial setup and launches the main GUI.

Repository: https://github.com/username/easy-claude-code
License: MIT
"""

import sys
import os
import shutil

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import aiohttp
        import tkinter
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required dependencies:")
        print("  pip install aiohttp")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, but you have {version.major}.{version.minor}")
        return False
    return True

def setup_config():
    """Setup configuration file if it doesn't exist"""
    config_file = "providers.json"
    example_file = "providers.example.json"
    
    if not os.path.exists(config_file):
        if os.path.exists(example_file):
            print("📋 Creating initial configuration from example...")
            shutil.copy(example_file, config_file)
            print(f"✅ Created {config_file}")
            print("🔧 Please edit providers.json with your API keys before using the application")
            return False
        else:
            print("⚠️ No configuration file found. The application will create a default one.")
    return True

def main():
    """Main entry point"""
    print("🚀 Easy Claude Code - AI Provider Switcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup configuration
    config_ready = setup_config()
    
    if not config_ready:
        print("\n📝 Next steps:")
        print("1. Edit providers.json with your API keys")
        print("2. Run this script again to launch the GUI")
        sys.exit(0)
    
    # Launch the GUI
    print("🎨 Launching GUI...")
    try:
        from gui_switcher_v2 import AIProviderGUI_V2
        import tkinter as tk
        
        # Create and run the GUI
        app = AIProviderGUI_V2()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print("Please check the error message and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()