#!/usr/bin/env python3
"""
自动修复 P0 格式问题
支持批量修复未闭合的粗体标记和标题层级跳跃
"""
import re
import os
import shutil
from pathlib import Path
from typing import List, Dict, Tuple


class AutoFixer:
    """自动修复器"""

    def __init__(self, vault_path: str, dry_run: bool = False):
        self.vault_path = Path(vault_path)
        self.dry_run = dry_run
        self.fixed_files = []
        self.total_fixes = 0

    def fix_unclosed_bold(self, content: str) -> Tuple[str, int]:
        """修复未闭合的粗体标记"""
        lines = content.split('\n')
        fixed_lines = []
        fixes = 0

        for line in lines:
            fixed_line = line
            bold_count = line.count('**')

            # 如果 ** 的数量是奇数，说明未闭合
            if bold_count % 2 != 0 and bold_count > 0:
                # 在行尾添加 ** 来闭合
                fixed_line = line.rstrip() + ' **'
                fixes += 1

            fixed_lines.append(fixed_line)

        return '\n'.join(fixed_lines), fixes

    def fix_heading_levels(self, content: str) -> Tuple[str, int]:
        """修复标题层级跳跃"""
        lines = content.split('\n')
        fixed_lines = []
        fixes = 0
        prev_level = 0
        heading_pattern = re.compile(r'^(#{1,6})\s*(.*?)\s*$')

        for line in lines:
            fixed_line = line
            match = heading_pattern.match(line)

            if match:
                level = len(match.group(1))
                content_text = match.group(2)

                # 如果层级跳跃超过1级，调整到合理的层级
                if prev_level > 0 and level > prev_level + 1:
                    new_level = prev_level + 1
                    new_heading = '#' * new_level + ' ' + content_text
                    fixed_line = new_heading
                    fixes += 1
                    level = new_level

                prev_level = level
            else:
                # 非标题行，重置 prev_level
                prev_level = 0

            fixed_lines.append(fixed_line)

        return '\n'.join(fixed_lines), fixes

    def fix_file(self, file_path: Path) -> int:
        """修复单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            content = original_content
            total_fixes = 0

            # 修复未闭合的粗体标记
            content, bold_fixes = self.fix_unclosed_bold(content)
            total_fixes += bold_fixes

            # 修复标题层级
            content, heading_fixes = self.fix_heading_levels(content)
            total_fixes += heading_fixes

            # 如果有修复，写入文件
            if total_fixes > 0 and content != original_content:
                if not self.dry_run:
                    # 备份原文件
                    backup_path = Path(str(file_path) + '.p0bak')
                    shutil.copy2(file_path, backup_path)

                    # 写入修复后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                self.fixed_files.append({
                    'file': str(file_path.relative_to(self.vault_path)),
                    'fixes': total_fixes
                })
                self.total_fixes += total_fixes
                return total_fixes

            return 0

        except Exception as e:
            print(f"⚠️  处理文件 {file_path} 时出错: {e}")
            return 0

    def fix_all(self, pattern: str = "*.md") -> Dict:
        """修复所有 Markdown 文件"""
        md_files = list(self.vault_path.rglob(pattern))
        total_files = len(md_files)

        print(f"🔧 开始修复 {total_files} 个文件...")
        print(f"模式: {'🧪 干运行（不修改文件）' if self.dry_run else '✅ 实际修复'}\n")

        for i, file_path in enumerate(md_files, 1):
            if i % 50 == 0:
                print(f"进度: {i}/{total_files}")

            self.fix_file(file_path)

        return {
            'total_files': total_files,
            'fixed_files': len(self.fixed_files),
            'total_fixes': self.total_fixes,
            'files_detail': self.fixed_files
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description='自动修复 P0 格式问题')
    parser.add_argument('--dir', required=True, help='Obsidian Vault 目录路径')
    parser.add_argument('--dry-run', action='store_true', help='干运行模式，不实际修改文件')
    parser.add_argument('--pattern', default='*.md', help='文件名模式（默认：*.md）')

    args = parser.parse_args()

    fixer = AutoFixer(args.dir, dry_run=args.dry_run)
    result = fixer.fix_all(args.pattern)

    print(f"\n{'='*60}")
    print(f"📊 修复完成统计")
    print(f"{'='*60}")
    print(f"扫描文件数: {result['total_files']}")
    print(f"修复文件数: {result['fixed_files']}")
    print(f"总修复数: {result['total_fixes']}")

    if result['fixed_files'] > 0:
        print(f"\n📋 修复文件列表（前20个）：")
        for item in result['files_detail'][:20]:
            print(f"  - {item['file']}: {item['fixes']} 处修复")

        if len(result['files_detail']) > 20:
            print(f"  ... 还有 {len(result['files_detail']) - 20} 个文件")

    if not args.dry_run:
        print(f"\n💾 备份文件已保存为 .p0bak 后缀")
        print(f"⚠️  如需回滚，请手动恢复备份文件")


if __name__ == '__main__':
    main()
