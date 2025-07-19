import os
import sys
import json
from pathlib import Path

def generate_html_directory_tree(start_path, output_file="directory_tree.html"):
    """
    生成带有可折叠目录结构的HTML文件
    :param start_path: 要遍历的根目录
    :param output_file: 输出的HTML文件名
    """
    # 生成目录数据
    directory_data = generate_directory_data(start_path)
    
    # 将目录数据转换为JSON字符串
    json_data = json.dumps(directory_data, ensure_ascii=False)
    
    # HTML模板 - 修复了JavaScript部分的变量引用问题
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>目录结构: {start_path}</title>
    <style>
        body {{
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
            background-color: #f8f9fa;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        ul {{
            list-style-type: none;
            padding-left: 20px;
        }}
        .folder {{
            cursor: pointer;
            position: relative;
            padding-left: 20px;
        }}
        .folder::before {{
            content: '📁 ';
        }}
        .folder.collapsed::before {{
            content: '📂 ';
        }}
        .file {{
            padding-left: 40px;
            color: #555;
        }}
        .file::before {{
            content: '📄 ';
        }}
        .folder-items {{
            display: block;
        }}
        .folder.collapsed + .folder-items {{
            display: none;
        }}
        .folder-toggle {{
            position: absolute;
            left: 0;
            cursor: pointer;
        }}
        .search-box {{
            margin: 15px 0;
            padding: 8px 12px;
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .highlight {{
            background-color: yellow;
            font-weight: bold;
        }}
        .file-count {{
            font-size: 14px;
            color: #777;
            margin-top: 10px;
            padding: 5px;
            background-color: #f0f0f0;
            border-radius: 4px;
        }}
        .path-info {{
            font-family: monospace;
            background-color: #f5f5f5;
            padding: 5px;
            border-radius: 3px;
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📂 目录结构: <span class="path-info">{start_path}</span></h1>
        
        <div>
            <input type="text" id="searchInput" class="search-box" placeholder="输入文件名进行搜索...">
            <button onclick="searchFiles()">搜索</button>
            <button onclick="clearSearch()">清除</button>
        </div>
        
        <div class="file-count">总文件夹: <span id="folderCount">0</span> | 总文件: <span id="fileCount">0</span></div>
        
        <div id="directoryTree"></div>
    </div>

    <script>
        // 初始目录树数据
        const directoryData = {json_data};
        
        // 统计信息
        document.getElementById('folderCount').textContent = directoryData.folderCount;
        document.getElementById('fileCount').textContent = directoryData.fileCount;
        
        // 渲染目录树
        function renderDirectoryTree(data, container) {{
            const ul = document.createElement('ul');
            
            data.items.forEach(item => {{
                const li = document.createElement('li');
                
                if (item.type === 'folder') {{
                    const folderDiv = document.createElement('div');
                    folderDiv.className = 'folder';
                    folderDiv.textContent = item.name;
                    folderDiv.onclick = function() {{ toggleFolder(this); }};
                    li.appendChild(folderDiv);
                    
                    const subContainer = document.createElement('div');
                    subContainer.className = 'folder-items';
                    li.appendChild(subContainer);
                    
                    if (item.items && item.items.length > 0) {{
                        renderDirectoryTree(item, subContainer);
                    }}
                }} else {{
                    const fileDiv = document.createElement('div');
                    fileDiv.className = 'file';
                    
                    const fileLink = document.createElement('a');
                    fileLink.href = item.path;
                    fileLink.target = '_blank';
                    fileLink.textContent = item.name;
                    
                    fileDiv.appendChild(fileLink);
                    li.appendChild(fileDiv);
                }}
                
                ul.appendChild(li);
            }});
            
            container.appendChild(ul);
        }}
        
        // 初始渲染
        renderDirectoryTree(directoryData, document.getElementById('directoryTree'));
        
        // 文件夹展开/折叠功能
        function toggleFolder(element) {{
            element.classList.toggle('collapsed');
            const folderItems = element.nextElementSibling;
            folderItems.style.display = element.classList.contains('collapsed') ? 'none' : 'block';
        }}
        
        // 搜索功能
        function searchFiles() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            if (!searchTerm) return;
            
            // 移除之前的高亮
            document.querySelectorAll('.highlight').forEach(el => {{
                el.classList.remove('highlight');
            }});
            
            // 查找匹配项
            const matches = [];
            document.querySelectorAll('.file, .folder').forEach(element => {{
                const text = element.textContent.toLowerCase();
                if (text.includes(searchTerm)) {{
                    element.classList.add('highlight');
                    matches.push(element);
                    
                    // 展开所有父文件夹
                    let parent = element.closest('.folder-items');
                    while (parent) {{
                        const folder = parent.previousElementSibling;
                        if (folder && folder.classList.contains('folder')) {{
                            folder.classList.remove('collapsed');
                        }}
                        parent = parent.parentElement.closest('.folder-items');
                    }}
                }}
            }});
            
            if (matches.length === 0) {{
                alert('未找到匹配的文件或文件夹');
            }}
        }}
        
        // 清除搜索
        function clearSearch() {{
            document.getElementById('searchInput').value = '';
            document.querySelectorAll('.highlight').forEach(el => {{
                el.classList.remove('highlight');
            }});
        }}
        
        // 页面加载时折叠所有文件夹
        window.onload = function() {{
            document.querySelectorAll('.folder').forEach(folder => {{
                folder.classList.add('collapsed');
            }});
        }};
    </script>
</body>
</html>
"""

    # 将生成的HTML写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    return output_file

def generate_directory_data(path, relative_to=None):
    """
    生成目录结构的JSON数据
    :param path: 当前路径
    :param relative_to: 相对路径基准
    :return: 包含目录结构的字典
    """
    if relative_to is None:
        relative_to = path
    
    path_obj = Path(path)
    data = {
        "name": path_obj.name,
        "path": os.path.relpath(path, relative_to) if path != relative_to else ".",
        "type": "folder",
        "items": [],
        "folderCount": 0,
        "fileCount": 0
    }
    
    try:
        # 遍历目录内容
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                # 递归处理子目录
                sub_data = generate_directory_data(entry.path, relative_to)
                data["items"].append(sub_data)
                data["folderCount"] += sub_data["folderCount"] + 1
                data["fileCount"] += sub_data["fileCount"]
            elif entry.is_file():
                # 添加文件
                data["items"].append({
                    "name": entry.name,
                    "path": os.path.relpath(entry.path, relative_to),
                    "type": "file"
                })
                data["fileCount"] += 1
    
    except PermissionError:
        # 处理权限问题
        data["items"].append({
            "name": "⚠️ 无法访问 (权限不足)",
            "type": "error"
        })
    except Exception as e:
        # 处理其他异常
        data["items"].append({
            "name": f"⚠️ 错误: {str(e)}",
            "type": "error"
        })
    
    # 按类型排序：文件夹在前，文件在后
    data["items"].sort(key=lambda x: (x["type"] != "folder", x["name"].lower()))
    
    return data

if __name__ == "__main__":
    # 获取当前目录
    current_dir = os.getcwd()
    
    # 生成HTML文件名
    dir_name = os.path.basename(current_dir)
    output_file = f"{dir_name}_目录结构.html"
    
    print(f"正在生成目录结构: {current_dir}")
    html_file = generate_html_directory_tree(current_dir, output_file)
    
    # 获取绝对路径
    abs_path = os.path.abspath(html_file)
    
    print(f"生成完成! 已创建: {html_file}")
    print(f"绝对路径: {abs_path}")
    print("请用浏览器打开该HTML文件查看目录结构")