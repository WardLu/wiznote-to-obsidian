#!/usr/bin/env python3
"""
转换 Markdown 链接为 Obsidian WikiLinks
"""
import re
import os
from pathlib import Path

def convert_markdown_links_to_wikilinks(file_path):
    """转换文件中的 markdown 链接为 wikilinks"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 匹配 [text](path/to/file.md) 格式
    # 转换为 [[file|text]] 或 [[text]]（如果 text 就是文件名）
    def replace_link(match):
        text = match.group(1)
        path = match.group(2)

        # 提取文件名（不含路径和扩展名）
        filename = os.path.basename(path)
        if filename.endswith('.md'):
            filename = filename[:-3]

        # 如果 text 和文件名相同或相似，使用 [[filename]]
        # 否则使用 [[filename|text]]
        if filename in text or text == filename:
            return f"[[{filename}]]"
        else:
            return f"[[{filename}|{text}]]"

    # 匹配 markdown 链接模式
    pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
    content = re.sub(pattern, replace_link, content)

    # 如果有修改，写回文件
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    vault_path = "/Users/wardlu/Documents/Obsidian Vault/02_Areas"
    converted_count = 0
    total_links = 0

    # 遍历所有 .md 文件
    for md_file in Path(vault_path).rglob('*.md'):
        if convert_markdown_links_to_wikilinks(md_file):
            converted_count += 1
            # 统计转换的链接数
            with open(md_file, 'r', encoding='utf-8') as f:
                total_links += len(re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', f.read()))

    print(f"✅ 转换完成！")
    print(f"   - 修改的文件数: {converted_count}")
    print(f"   - WikiLinks 总数: {total_links}")

if __name__ == '__main__':
    main()
