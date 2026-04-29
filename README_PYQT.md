# Markdown Editor - PyQt5 Desktop Application

一个功能完整的桌面端 Markdown 编辑器，支持实时预览。

## 功能特性

✅ **左右分屏设计** - 左侧编辑区，右侧预览区，窗口最大化时自动扩展
✅ **实时预览** - 输入后 500ms 自动刷新预览（支持暂停）
✅ **文件操作** - 新建、打开、保存 Markdown 文件
✅ **丰富语法** - 支持表格、代码高亮、引用、列表等
✅ **键盘快捷键** - Ctrl+N/O/S/R 快速操作
✅ **状态栏** - 显示字符数和行数统计

## 运行方式

### 方法 1：直接运行 Python 脚本
```bash
python markdown_editor_pyqt.py              # 新建文档
python markdown_editor_pyqt.py sample.md    # 打开现有文件
```

### 方法 2：打包为独立可执行文件
```bash
# 安装依赖
pip install PyQt5 markdown PyInstaller

# 打包应用
pyinstaller MarkdownEditorPyQt.spec --noconfirm

# 运行可执行文件
./dist/MarkdownEditor
./dist/MarkdownEditor sample.md
```

## 系统要求

- Python 3.8+
- PyQt5
- Markdown
- 支持 Windows、macOS、Linux

## 使用说明

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建文档 |
| Ctrl+O | 打开文件 |
| Ctrl+S | 保存文件 |
| Ctrl+R | 刷新预览 |

## 主要改进

相比之前的 webview 版本，PyQt5 版本解决了以下问题：

1. **窗口最大化问题** - 使用 QSplitter 实现真正的弹性布局，窗口最大化时编辑区和预览区会自动扩展
2. **原生桌面应用** - 基于 PyQt5 构建，是真正的桌面应用程序，不是 Web 包装
3. **更好的性能** - 原生控件，响应更快
4. **更丰富的功能** - 状态栏、快捷键、工具栏等

## 截图功能

- 工具栏包含：新建、打开、保存、刷新、暂停自动刷新
- 编辑器使用等宽字体，适合代码编写
- 预览区支持完整的 Markdown 渲染样式
