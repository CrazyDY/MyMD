#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown Editor - A simple PC markdown editor with live preview
"""

import os
import sys
import webview
import markdown
from pathlib import Path


class MarkdownEditor:
    def __init__(self):
        self.current_file = None
        self.content = ""
        
    def load_file(self, file_path):
        """Load markdown content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self.current_file = file_path
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def save_file(self, file_path=None):
        """Save markdown content to file"""
        if file_path is None:
            file_path = self.current_file
        
        if file_path is None:
            return False
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            return True
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
    
    def get_html(self):
        """Convert markdown to HTML"""
        md = markdown.Markdown(extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br'
        ])
        html_body = md.convert(self.content)
        
        # Complete HTML template with CSS styling
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 900px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    margin-top: 1.5em;
                    margin-bottom: 0.5em;
                }}
                h1 {{ border-bottom: 2px solid #3498db; padding-bottom: 0.3em; }}
                h2 {{ border-bottom: 1px solid #bdc3c7; padding-bottom: 0.3em; }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', Courier, monospace;
                }}
                pre {{
                    background-color: #2d2d2d;
                    color: #f8f8f2;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                    color: inherit;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 1em 0;
                    padding-left: 1em;
                    color: #666;
                    background-color: #f9f9f9;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 1em 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
                a {{
                    color: #3498db;
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                }}
                ul, ol {{
                    padding-left: 2em;
                }}
                hr {{
                    border: none;
                    border-top: 1px solid #ddd;
                    margin: 2em 0;
                }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        return html_template
    
    def update_content(self, new_content):
        """Update the markdown content"""
        self.content = new_content


# Global editor instance
editor = MarkdownEditor()


def get_content():
    """API: Get current markdown content"""
    return editor.content


def set_content(new_content):
    """API: Set new markdown content from editor"""
    editor.update_content(new_content)


def get_html_preview():
    """API: Get HTML preview of current content"""
    return editor.get_html()


def load_file_dialog():
    """API: Open file dialog and load selected file"""
    try:
        file_path = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False
        )
        if file_path and len(file_path) > 0:
            file_path = file_path[0]
            if editor.load_file(file_path):
                return editor.content
        return None
    except Exception as e:
        print(f"Error in file dialog: {e}")
        return None


def save_file_dialog(content):
    """API: Open save dialog and save content"""
    try:
        editor.update_content(content)
        file_path = webview.windows[0].create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename='document.md' if not editor.current_file else os.path.basename(editor.current_file)
        )
        if file_path and len(file_path) > 0:
            file_path = file_path[0]
            if editor.save_file(file_path):
                return True
        return False
    except Exception as e:
        print(f"Error in save dialog: {e}")
        return False


def create_main_window():
    """Create the main application window with split view"""
    
    # HTML for the editor interface
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                display: flex;
                flex-direction: column;
                height: 100vh;
                background: #f5f5f5;
            }
            .toolbar {
                background: #2c3e50;
                padding: 10px 20px;
                display: flex;
                gap: 10px;
                align-items: center;
            }
            .toolbar button {
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
            }
            .toolbar button:hover {
                background: #2980b9;
            }
            .container {
                display: flex;
                flex: 1;
                overflow: hidden;
            }
            .editor-pane, .preview-pane {
                flex: 1;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            .editor-pane {
                border-right: 2px solid #ddd;
            }
            .pane-header {
                background: #ecf0f1;
                padding: 8px 15px;
                font-weight: bold;
                color: #2c3e50;
                border-bottom: 1px solid #ddd;
            }
            #editor {
                flex: 1;
                width: 100%;
                padding: 15px;
                border: none;
                resize: none;
                font-family: 'Courier New', Courier, monospace;
                font-size: 14px;
                line-height: 1.6;
                outline: none;
                background: #fff;
            }
            #preview {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                background: #fff;
                border: none;
            }
            iframe {
                width: 100%;
                height: 100%;
                border: none;
            }
        </style>
    </head>
    <body>
        <div class="toolbar">
            <button onclick="loadFile()">📂 Open</button>
            <button onclick="saveFile()">💾 Save</button>
            <button onclick="updatePreview()">🔄 Refresh Preview</button>
        </div>
        <div class="container">
            <div class="editor-pane">
                <div class="pane-header">✏️ Editor</div>
                <textarea id="editor" placeholder="Write your markdown here..."></textarea>
            </div>
            <div class="preview-pane">
                <div class="pane-header">👁️ Preview</div>
                <div id="preview"></div>
            </div>
        </div>
        
        <script>
            let updateTimeout;
            
            // Initialize
            window.onload = function() {
                loadContent();
            };
            
            // Load content from Python
            async function loadContent() {
                try {
                    const content = await pywebview.api.get_content();
                    document.getElementById('editor').value = content || '';
                    updatePreview();
                } catch (e) {
                    console.error('Error loading content:', e);
                }
            }
            
            // Update preview
            async function updatePreview() {
                try {
                    const content = document.getElementById('editor').value;
                    await pywebview.api.set_content(content);
                    const html = await pywebview.api.get_html_preview();
                    const previewDiv = document.getElementById('preview');
                    previewDiv.innerHTML = html;
                } catch (e) {
                    console.error('Error updating preview:', e);
                }
            }
            
            // Auto-update preview on typing (debounced)
            document.getElementById('editor').addEventListener('input', function() {
                clearTimeout(updateTimeout);
                updateTimeout = setTimeout(updatePreview, 500);
            });
            
            // Load file
            async function loadFile() {
                try {
                    const content = await pywebview.api.load_file_dialog();
                    if (content !== null) {
                        document.getElementById('editor').value = content;
                        updatePreview();
                    }
                } catch (e) {
                    console.error('Error loading file:', e);
                }
            }
            
            // Save file
            async function saveFile() {
                try {
                    const content = document.getElementById('editor').value;
                    const success = await pywebview.api.save_file_dialog(content);
                    if (success) {
                        alert('File saved successfully!');
                    } else {
                        alert('Failed to save file.');
                    }
                } catch (e) {
                    console.error('Error saving file:', e);
                    alert('Error saving file: ' + e.message);
                }
            }
        </script>
    </body>
    </html>
    """
    
    # Create API class for JavaScript-Python communication
    class Api:
        def get_content(self):
            return get_content()
        
        def set_content(self, content):
            set_content(content)
        
        def get_html_preview(self):
            return get_html_preview()
        
        def load_file_dialog(self):
            return load_file_dialog()
        
        def save_file_dialog(self, content):
            return save_file_dialog(content)
    
    # Create window
    window = webview.create_window(
        'Markdown Editor',
        html=html_content,
        js_api=Api(),
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False
    )
    
    return window


def main():
    """Main entry point"""
    print("Starting Markdown Editor...")
    
    # Check if a file was passed as argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            editor.load_file(file_path)
            print(f"Loaded file: {file_path}")
        else:
            print(f"File not found: {file_path}")
    
    # Create and start the application
    window = create_main_window()
    webview.start(debug=False)


if __name__ == '__main__':
    main()
