#!/usr/bin/env python3
"""
修复图片路径 - 根据实际文件位置建立映射
"""
import re
from pathlib import Path
import hashlib

def find_image_by_name(attachments_dir, image_name):
    """在 attachments 目录中查找图片"""
    matches = list(attachments_dir.rglob(image_name))
    if matches:
        # 返回相对路径
        return str(matches[0].relative_to(attachments_dir))
    return None

def fix_image_paths():
    vault_path = Path("/Users/wardlu/Documents/Obsidian Vault/02_Areas")
    attachments_dir = Path("/Users/wardlu/Documents/Obsidian Vault/Wiznote/attachments")

    print("🔧 开始修复图片路径...")

    fixed_count = 0
    not_found_count = 0

    # 遍历所有 markdown 文件
    for md_file in vault_path.rglob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        images_in_file = re.findall(r'!\[\(/Wiznote/attachments/images/([^)]+)\)', content)

        for image_name in images_in_file:
            # 在 attachments 目录中查找图片
            relative_path = find_image_by_name(attachments_dir, image_name)

            if relative_path:
                # 替换为正确的路径
                old_path = f'![](/Wiznote/attachments/images/{image_name})'
                new_path = f'![](/Wiznote/attachments/{relative_path})'
                content = content.replace(old_path, new_path)
                fixed_count += 1
                print(f"  ✅ {image_name} → {relative_path}")
            else:
                not_found_count += 1
                print(f"  ❌ 未找到: {image_name}")

        # 只在有修改时写入文件
        if content != original_content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)

    print(f"\n📊 修复完成:")
    print(f"   - 已修复: {fixed_count} 个图片路径")
    print(f"   - 未找到: {not_found_count} 个图片")

if __name__ == '__main__':
    fix_image_paths()
