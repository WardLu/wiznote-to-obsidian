#!/usr/bin/env python3
"""
为 WizNote 导出的 Obsidian 文件添加或更新 YAML front matter
"""

import os
import re
from datetime import datetime
from pathlib import Path

# 文件分类映射
CATEGORIES = {
    "求职/Wiznote面试材料": {
        "tags": ["Wiznote", "求职", "面试", "⭐⭐⭐⭐⭐"],
        "category": "职业发展"
    },
    "职业发展/年度总结": {
        "tags": ["Wiznote", "年度总结", "职业发展", "⭐⭐⭐⭐⭐"],
        "category": "职业发展"
    },
    "职业发展/智布互联": {
        "tags": ["Wiznote", "工作日志", "智布互联", "⭐⭐⭐⭐"],
        "category": "职业发展"
    },
    "职业发展/唯衣网络": {
        "tags": ["Wiznote", "工作日志", "唯衣网络", "⭐⭐⭐⭐"],
        "category": "职业发展"
    },
    "产品思考/B端产品": {
        "tags": ["Wiznote", "读书笔记", "B端产品", "⭐⭐⭐⭐⭐"],
        "category": "产品思考"
    },
    "产品思考/产品管理": {
        "tags": ["Wiznote", "产品管理", "方法论", "⭐⭐⭐⭐"],
        "category": "产品思考"
    },
    "阅读/Books/产品管理": {
        "tags": ["Wiznote", "读书笔记", "产品管理", "⭐⭐⭐⭐⭐"],
        "category": "阅读"
    }
}

def extract_existing_front_matter(content):
    """提取现有的 front matter"""
    front_matter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if front_matter_match:
        return front_matter_match.group(1), content[front_matter_match.end():]
    return None, content

def parse_created_date(front_matter_text):
    """从旧的 front matter 中解析创建日期"""
    if not front_matter_text:
        return None

    # 尝试解析 date 字段（可能是时间戳）
    date_match = re.search(r'date:\s*(\d+)', front_matter_text)
    if date_match:
        timestamp = int(date_match.group(1))
        try:
            return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
        except:
            pass

    return None

def clean_filename(filename):
    """清理文件名，去除 .md.md 双重扩展名"""
    if filename.endswith('.md.md'):
        return filename[:-3]  # 去掉最后的 .md
    return filename

def generate_front_matter(filename, relative_path, existing_front_matter=None):
    """生成新的 YAML front matter"""
    # 确定分类
    category_info = None
    for category_path, info in CATEGORIES.items():
        if category_path in relative_path:
            category_info = info
            break

    if not category_info:
        category_info = {"tags": ["Wiznote", "⭐⭐⭐"], "category": "其他"}

    # 清理文件名作为标题
    title = clean_filename(filename)
    if title.endswith('.md'):
        title = title[:-3]

    # 解析创建日期
    created_date = parse_created_date(existing_front_matter) if existing_front_matter else None
    if not created_date:
        created_date = "2020-01-01"  # 默认日期

    # 生成 front matter
    front_matter = f"""---
title: "{title}"
created: {created_date}
imported: 2026-02-01
source: Wiznote
original_path: "{relative_path}"
tags: {str(category_info["tags"])}
value: high
status: archived
category: "{category_info["category"]}"
---

"""
    return front_matter

def process_file(file_path, vault_root):
    """处理单个文件"""
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 获取相对路径
        rel_path = os.path.relpath(file_path, vault_root)
        filename = os.path.basename(file_path)

        # 提取现有的 front matter
        existing_front_matter, body_content = extract_existing_front_matter(content)

        # 生成新的 front matter
        new_front_matter = generate_front_matter(filename, rel_path, existing_front_matter)

        # 组合新内容
        new_content = new_front_matter + body_content

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, filename
    except Exception as e:
        return False, f"{filename}: {str(e)}"

def main():
    vault_root = "/Users/wardlu/Documents/Obsidian Vault/02_Areas"
    processed_count = 0
    error_count = 0
    errors = []

    # 遍历所有目标目录
    target_dirs = [
        "求职/Wiznote面试材料",
        "职业发展/年度总结",
        "职业发展/智布互联",
        "职业发展/唯衣网络",
        "产品思考/B端产品",
        "产品思考/产品管理",
        "阅读/Books/产品管理"
    ]

    print("🚀 开始处理文件...")
    print("=" * 60)

    for dir_path in target_dirs:
        full_path = os.path.join(vault_root, dir_path)
        if not os.path.exists(full_path):
            print(f"⚠️  跳过不存在的目录: {dir_path}")
            continue

        print(f"\n📁 处理目录: {dir_path}")
        print("-" * 60)

        # 遍历目录中的所有 .md 文件
        for filename in os.listdir(full_path):
            if filename.endswith('.md'):
                file_path = os.path.join(full_path, filename)
                success, result = process_file(file_path, vault_root)

                if success:
                    print(f"  ✅ {result}")
                    processed_count += 1
                else:
                    print(f"  ❌ {result}")
                    error_count += 1
                    errors.append(result)

    print("\n" + "=" * 60)
    print(f"✨ 处理完成！")
    print(f"  📊 成功处理: {processed_count} 个文件")
    print(f"  ❌ 处理失败: {error_count} 个文件")

    if errors:
        print(f"\n❌ 错误详情:")
        for error in errors:
            print(f"  - {error}")

if __name__ == "__main__":
    main()
