#!/usr/bin/env python3
"""
生成 WizNote 到 Obsidian 转换的详细统计报告
"""
import os
from pathlib import Path
import re

def generate_report():
    vault_path = "/Users/wardlu/Documents/Obsidian Vault/02_Areas"
    attachments_path = "/Users/wardlu/Documents/Obsidian Vault/Wiznote/attachments"

    print("=" * 60)
    print("📊 WizNote → Obsidian 转换报告")
    print("=" * 60)

    # 1. 统计 markdown 文件
    md_files = list(Path(vault_path).rglob('*.md'))
    print(f"\n📝 Markdown 文件统计:")
    print(f"   - 总文件数: {len(md_files)}")

    # 2. 统计图片
    image_files = list(Path(attachments_path).rglob('*'))
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    images = [f for f in image_files if f.suffix.lower() in image_extensions]
    print(f"\n🖼️  图片统计:")
    print(f"   - 总图片数: {len(images)}")
    print(f"   - 占用空间: {sum(f.stat().st_size for f in images) / 1024 / 1024:.2f} MB")

    # 3. 统计图片链接
    image_links = 0
    wikilinks = 0
    callouts = 0
    highlights = 0

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            image_links += len(re.findall(r'!\[\(/Wiznote/attachments/', content))
            wikilinks += len(re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', content))
            callouts += len(re.findall(r'> \[!\w+\]', content))
            highlights += len(re.findall(r'==[^=]+==', content))

    print(f"\n🔗 链接统计:")
    print(f"   - 图片链接: {image_links}")
    print(f"   - WikiLinks: {wikilinks}")

    print(f"\n✨ Obsidian 增强特性:")
    print(f"   - Callouts: {callouts}")
    print(f"   - 关键词高亮: {highlights}")

    # 4. 文件分类统计
    categories = {}
    for md_file in md_files:
        category = md_file.parent.name
        categories[category] = categories.get(category, 0) + 1

    print(f"\n📂 文件分类 (Top 10):")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   - {cat}: {count} 个文件")

    # 5. 增强的核心文件
    print(f"\n🎨 已增强的核心文件:")
    enhanced_files = [
        "产品思考/B端产品/决胜B端读书笔记.md",
        "求职/Wiznote面试材料/2025高级产品经理面试.md"
    ]
    for file_path in enhanced_files:
        full_path = Path(vault_path) / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (不存在)")

    # 6. 验证检查
    print(f"\n🔍 验证检查:")

    # 检查是否还有未修复的相对路径
    relative_path_count = 0
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            relative_path_count += len(re.findall(r'\]\(images/', content))

    if relative_path_count == 0:
        print(f"   ✅ 所有图片路径已转换为绝对路径")
    else:
        print(f"   ⚠️  仍有 {relative_path_count} 个相对路径未转换")

    # 检查双重扩展名
    double_ext = list(Path(vault_path).rglob('*.md.md'))
    if len(double_ext) == 0:
        print(f"   ✅ 所有双重扩展名已修复")
    else:
        print(f"   ⚠️  仍有 {len(double_ext)} 个文件存在双重扩展名")

    print("\n" + "=" * 60)
    print("🎉 转换完成！")
    print("=" * 60)

    print("\n📋 增强特性说明:")
    print("   1. 图片路径: ](/Wiznote/attachments/...) → Obsidian 绝对路径")
    print("   2. WikiLinks: [[文件名]] 或 [[文件名|显示文本]]")
    print("   3. 关键词高亮: ==关键词==")
    print("   4. Callouts: > [!TIP], > [!IMPORTANT], > [!QUOTE]")
    print("   5. 折叠块: <details><summary>...</summary>...</details>")

    print("\n💡 下一步建议:")
    print("   1. 在 Obsidian 中打开 '决胜B端读书笔记.md' 验证效果")
    print("   2. 检查图片是否正常显示")
    print("   3. 根据需要继续为其他文件添加增强特性")

if __name__ == '__main__':
    generate_report()
