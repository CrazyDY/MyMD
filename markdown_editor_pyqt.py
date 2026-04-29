#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown Editor - A PyQt5 desktop markdown editor with live preview
Features:
- Split view (editor + preview)
- Live preview with auto-refresh
- Open/Save markdown files
- Rich markdown syntax support
"""

import sys
import os
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QSplitter, QToolBar, QAction, QFileDialog,
    QLabel, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QKeySequence

import markdown


class MarkdownEditor(QMainWindow):
    """Main window for the Markdown Editor"""
    
    def __init__(self, file_path=None):
        super().__init__()
        
        self.current_file = file_path
        self.content = ""
        self.auto_refresh_enabled = True
        
        # Timer for auto-refresh (debounce) - initialize before UI
        self.refresh_timer = QTimer()
        self.refresh_timer.setSingleShot(True)
        self.refresh_timer.timeout.connect(self.update_preview)
        
        # Initialize UI
        self.init_ui()
        
        # Load file if provided
        if file_path and os.path.exists(file_path):
            self.load_file(file_path)
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Markdown Editor")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Toolbar
        self.create_toolbar()
        
        # Splitter for editor and preview
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)
        
        # Editor pane
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        editor_label = QLabel("✏️ Editor")
        editor_label.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                padding: 8px 15px;
                font-weight: bold;
                color: #2c3e50;
                border-bottom: 1px solid #ddd;
            }
        """)
        editor_label.setFixedHeight(35)
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Courier New", 12))
        self.editor.setPlaceholderText("Write your markdown here...")
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 15px;
                background-color: #ffffff;
                selection-background-color: #3498db;
                selection-color: white;
            }
        """)
        
        editor_layout.addWidget(editor_label)
        editor_layout.addWidget(self.editor)
        
        # Preview pane
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(0)
        
        preview_label = QLabel("👁️ Preview")
        preview_label.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                padding: 8px 15px;
                font-weight: bold;
                color: #2c3e50;
                border-bottom: 1px solid #ddd;
            }
        """)
        preview_label.setFixedHeight(35)
        
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 15px;
                background-color: #ffffff;
            }
        """)
        
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.preview)
        
        # Add panes to splitter
        splitter.addWidget(editor_widget)
        splitter.addWidget(preview_widget)
        
        # Set initial sizes (50/50 split)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Keyboard shortcuts
        self.setup_shortcuts()
    
    def create_toolbar(self):
        """Create the toolbar with actions"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        from PyQt5.QtCore import QSize
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2c3e50;
                spacing: 10px;
                padding: 5px;
            }
            QToolButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 13px;
            }
            QToolButton:hover {
                background-color: #2980b9;
            }
            QToolButton:pressed {
                background-color: #1a5276;
            }
        """)
        self.addToolBar(toolbar)
        
        # New action
        new_action = QAction("📄 New", self)
        new_action.setStatusTip("Create a new document")
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)
        
        # Open action
        open_action = QAction("📂 Open", self)
        open_action.setStatusTip("Open a markdown file")
        open_action.triggered.connect(self.open_file_dialog)
        toolbar.addAction(open_action)
        
        # Save action
        save_action = QAction("💾 Save", self)
        save_action.setStatusTip("Save the current file")
        save_action.triggered.connect(self.save_file_dialog)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Refresh action
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.setStatusTip("Refresh the preview")
        refresh_action.triggered.connect(self.update_preview)
        toolbar.addAction(refresh_action)
        
        # Auto-refresh toggle
        self.auto_refresh_action = QAction("⏸️ Pause Auto-Refresh", self)
        self.auto_refresh_action.setStatusTip("Toggle auto-refresh on/off")
        self.auto_refresh_action.triggered.connect(self.toggle_auto_refresh)
        toolbar.addAction(self.auto_refresh_action)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Ctrl+N - New
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence(QKeySequence.New))
        new_action.triggered.connect(self.new_file)
        self.editor.addAction(new_action)
        
        # Ctrl+O - Open
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence(QKeySequence.Open))
        open_action.triggered.connect(self.open_file_dialog)
        self.editor.addAction(open_action)
        
        # Ctrl+S - Save
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence(QKeySequence.Save))
        save_action.triggered.connect(self.save_file_dialog)
        self.editor.addAction(save_action)
        
        # Ctrl+R - Refresh
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut(QKeySequence("Ctrl+R"))
        refresh_action.triggered.connect(self.update_preview)
        self.editor.addAction(refresh_action)
    
    def on_text_changed(self):
        """Handle text change in editor"""
        self.content = self.editor.toPlainText()
        
        if self.auto_refresh_enabled:
            # Debounce: wait 500ms after last keystroke
            self.refresh_timer.start(500)
        
        # Update status bar
        char_count = len(self.content)
        line_count = self.content.count('\n') + 1
        self.status_bar.showMessage(f"Characters: {char_count} | Lines: {line_count}")
    
    def update_preview(self):
        """Update the preview pane with rendered HTML"""
        try:
            md = markdown.Markdown(extensions=[
                'tables',
                'fenced_code',
                'codehilite',
                'nl2br'
            ])
            html_body = md.convert(self.content)
            
            # CSS styles for preview
            css_styles = """
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        padding: 10px;
                        background-color: #fff;
                    }
                    h1, h2, h3, h4, h5, h6 {
                        color: #2c3e50;
                        margin-top: 1.5em;
                        margin-bottom: 0.5em;
                    }
                    h1 { border-bottom: 2px solid #3498db; padding-bottom: 0.3em; }
                    h2 { border-bottom: 1px solid #bdc3c7; padding-bottom: 0.3em; }
                    code {
                        background-color: #f4f4f4;
                        padding: 2px 6px;
                        border-radius: 3px;
                        font-family: 'Courier New', Courier, monospace;
                        color: #e74c3c;
                    }
                    pre {
                        background-color: #2d2d2d;
                        color: #f8f8f2;
                        padding: 15px;
                        border-radius: 5px;
                        overflow-x: auto;
                    }
                    pre code {
                        background-color: transparent;
                        padding: 0;
                        color: inherit;
                    }
                    blockquote {
                        border-left: 4px solid #3498db;
                        margin: 1em 0;
                        padding-left: 1em;
                        color: #666;
                        background-color: #f9f9f9;
                    }
                    table {
                        border-collapse: collapse;
                        width: 100%;
                        margin: 1em 0;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px 12px;
                        text-align: left;
                    }
                    th {
                        background-color: #3498db;
                        color: white;
                    }
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                    a {
                        color: #3498db;
                        text-decoration: none;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    img {
                        max-width: 100%;
                        height: auto;
                    }
                    ul, ol {
                        padding-left: 2em;
                    }
                    hr {
                        border: none;
                        border-top: 1px solid #ddd;
                        margin: 2em 0;
                    }
                </style>
            """
            
            full_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    {css_styles}
                </head>
                <body>
                    {html_body}
                </body>
                </html>
            """
            
            self.preview.setHtml(full_html)
        except Exception as e:
            self.preview.setHtml(f"<p style='color: red;'>Error rendering preview: {str(e)}</p>")
    
    def new_file(self):
        """Create a new document"""
        if self.maybe_save():
            self.editor.clear()
            self.current_file = None
            self.content = ""
            self.update_preview()
            self.setWindowTitle("Markdown Editor")
            self.status_bar.showMessage("New document created")
    
    def open_file_dialog(self):
        """Open file dialog to select a markdown file"""
        if not self.maybe_save():
            return
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Markdown File",
            "",
            "Markdown Files (*.md *.markdown);;All Files (*)"
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path):
        """Load content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.current_file = file_path
            self.editor.setPlainText(content)
            self.content = content
            self.update_preview()
            
            filename = os.path.basename(file_path)
            self.setWindowTitle(f"{filename} - Markdown Editor")
            self.status_bar.showMessage(f"Loaded: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
    
    def save_file_dialog(self):
        """Save file dialog"""
        if self.current_file:
            self.save_file(self.current_file)
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Markdown File",
                "document.md",
                "Markdown Files (*.md *.markdown);;All Files (*)"
            )
            
            if file_path:
                self.save_file(file_path)
    
    def save_file(self, file_path):
        """Save content to a file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.setWindowTitle(f"{filename} - Markdown Editor")
            self.status_bar.showMessage(f"Saved: {file_path}")
            
            QMessageBox.information(self, "Success", "File saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")
    
    def maybe_save(self):
        """Check if unsaved changes exist and prompt to save"""
        # Simple implementation: always allow discard
        # Could be enhanced to track modifications
        return True
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh feature"""
        self.auto_refresh_enabled = not self.auto_refresh_enabled
        
        if self.auto_refresh_enabled:
            self.auto_refresh_action.setText("⏸️ Pause Auto-Refresh")
            self.status_bar.showMessage("Auto-refresh enabled")
        else:
            self.auto_refresh_action.setText("▶️ Enable Auto-Refresh")
            self.status_bar.showMessage("Auto-refresh disabled")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()


def main():
    """Main entry point"""
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Get file path from command line if provided
    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    # Create and show main window
    window = MarkdownEditor(file_path)
    window.show()
    
    # Maximize window by default
    window.showMaximized()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
