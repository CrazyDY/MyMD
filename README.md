# Markdown Editor

一个简单易用的 PC 端 Markdown 编辑器，支持实时预览。

## 功能特性

- ✏️ **编辑** - 左侧编辑区编写 Markdown 文本
- 👁️ **预览** - 右侧实时预览渲染后的 HTML 效果
- 📂 **打开文件** - 支持打开本地 .md 文件
- 💾 **保存文件** - 支持保存编辑内容到本地
- 🎨 **美观界面** - 简洁的分屏设计，舒适的阅读体验
- ⚡ **自动刷新** - 输入时自动更新预览（500ms 延迟）

## 依赖

```bash
pip install markdown pywebview
```

## 使用方法

### 直接运行
```bash
python markdown_editor.py
```

### 打开指定文件
```bash
python markdown_editor.py your_file.md
```

## 支持的 Markdown 语法

- 标题 (H1-H6)
- 粗体和斜体
- 代码块（带语法高亮）
- 表格
- 引用块
- 列表（有序和无序）
- 链接和图片
- 水平分割线

## 技术实现

- **前端**: HTML5 + CSS3 + JavaScript
- **后端**: Python 3
- **GUI 框架**: pywebview
- **Markdown 解析**: Python-Markdown

## 系统要求

- Python 3.8+
- 支持 WebKit/GTK/Qt 的操作系统（Windows/macOS/Linux）
