# macOS 构建资源

此目录用于存放 macOS 构建所需的资源文件：

## 图标文件

- `icon.icns` - 应用程序图标 (1024x1024 PNG 转换而来)
- `volume.icns` - DMG 卷标图标

## 创建图标的步骤：

1. 准备 1024x1024 的 PNG 图片
2. 使用 `iconutil` 工具转换为 icns 格式：
   ```bash
   iconutil -c icns -o icon.icns icon.png
   ```

## 注意事项

- 如果没有提供图标文件，构建脚本会使用默认图标
- 确保图标文件是 1024x1024 或更高分辨率
- 图标应该简洁明了，易于识别