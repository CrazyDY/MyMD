# Markdown Editor 桌面应用

这是一个完整的 PC 端 Markdown 编辑器桌面应用，支持编辑与实时预览。

## 📦 可执行文件

编译后的桌面应用位于：
- **Linux**: `dist/MarkdownEditor`

## 🚀 运行方式

### 方式一：直接运行可执行文件（推荐）
```bash
# Linux
./dist/MarkdownEditor

# 打开指定文件
./dist/MarkdownEditor your-file.md
```

### 方式二：通过 Python 运行源码
```bash
python markdown_editor.py
python markdown_editor.py your-file.md
```

## ✨ 功能特性

- 📝 **左右分屏**：左侧编辑，右侧实时预览
- ⚡ **实时预览**：输入后 500ms 自动刷新预览
- 📂 **文件操作**：支持打开和保存 Markdown 文件
- 🎨 **丰富样式**：支持表格、代码高亮、引用、列表等
- 🔧 **跨平台**：可在 Windows、macOS、Linux 上运行

## 🛠️ 重新打包

如果需要重新生成可执行文件：

```bash
# 安装依赖
pip install pyinstaller markdown pywebview

# Windows 打包
pyinstaller --onefile --windowed --name "MarkdownEditor" markdown_editor.py

# macOS 打包
pyinstaller --onefile --windowed --name "MarkdownEditor" markdown_editor.py

# Linux 打包
pyinstaller --onefile --windowed --name "MarkdownEditor" markdown_editor.py
```

## 📁 项目结构

```
markdown_editor/
├── dist/
│   └── MarkdownEditor      # 可执行文件
├── markdown_editor.py      # 源代码
├── README.md               # 说明文档
└── sample.md               # 示例文件
```

## 💡 使用说明

1. 双击运行 `MarkdownEditor` 可执行文件
2. 点击 "📂 Open" 按钮打开现有 Markdown 文件
3. 在左侧编辑器中编写 Markdown 内容
4. 右侧会自动显示预览效果
5. 点击 "💾 Save" 按钮保存文件

## 📋 支持的 Markdown 语法

- 标题（H1-H6）
- 粗体、斜体
- 代码块（带语法高亮）
- 表格
- 引用块
- 有序/无序列表
- 链接和图片
- 水平分割线
