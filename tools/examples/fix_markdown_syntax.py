#!/usr/bin/env python3
"""
Markdown 语法自动修复工具
批量修复 Obsidian Vault 中的 Markdown 文件语法问题
"""

import re
from pathlib import Path
from typing import List, Tuple

class MarkdownFixer:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.original_lines = []
        self.fixed_lines = []
        self.fixes_applied = []

    def fix(self) -> Tuple[List[str], List[str]]:
        """执行所有自动修复"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.original_lines = f.readlines()
            self.fixed_lines = self.original_lines.copy()
        except Exception as e:
            return [], [f'文件读取错误: {e}']

        # 执行各项修复
        self.fix_heading_spaces()
        self.fix_list_markers()
        self.fix_code_blocks()
        self.fix_blank_lines()
        self.fix_horizontal_rules()

        return self.fixed_lines, self.fixes_applied

    def fix_heading_spaces(self):
        """修复标题前后空格"""
        pattern = re.compile(r'^(#{1,6})([^\s#])')

        for i, line in enumerate(self.fixed_lines):
            new_line = pattern.sub(r'\1 \2', line)
            if new_line != line:
                self.fixed_lines[i] = new_line
                self.fixes_applied.append(f'第 {i+1} 行: 修复标题空格')

    def fix_list_markers(self):
        """统一无序列表标记为 -"""
        pattern = re.compile(r'^(\s*)\* ')

        for i, line in enumerate(self.fixed_lines):
            # 不在代码块内
            if not self._is_in_code_block(i):
                new_line = pattern.sub(r'\1- ', line)
                if new_line != line:
                    self.fixed_lines[i] = new_line
                    self.fixes_applied.append(f'第 {i+1} 行: 统一列表标记为 -')

    def fix_code_blocks(self):
        """将缩进代码块转换为 fenced code blocks"""
        for i, line in enumerate(self.fixed_lines):
            # 检查是否是4空格缩进的代码行
            if line.startswith('    ') and not line.startswith('   \n'):
                # 检查前后是否有代码块标记
                has_fence_before = False
                has_fence_after = False

                for j in range(i-1, max(0, i-5), -1):
                    if self.fixed_lines[j].strip().startswith('```'):
                        has_fence_before = True
                        break
                    if self.fixed_lines[j].strip():
                        break

                for j in range(i+1, min(len(self.fixed_lines), i+5)):
                    if self.fixed_lines[j].strip().startswith('```'):
                        has_fence_after = True
                        break
                    if self.fixed_lines[j].strip():
                        break

                if not has_fence_before:
                    # 查找连续的缩进行
                    start_line = i
                    end_line = i

                    for j in range(i+1, len(self.fixed_lines)):
                        if self.fixed_lines[j].startswith('    ') or self.fixed_lines[j].strip() == '':
                            end_line = j
                        else:
                            break

                    # 如果有多行，添加代码块标记
                    if end_line > start_line or (start_line == end_line and self.fixed_lines[start_line].strip()):
                        self.fixed_lines[start_line] = '```\n' + self.fixed_lines[start_line]

                        # 移除缩进
                        for j in range(start_line, end_line + 1):
                            if self.fixed_lines[j].startswith('    '):
                                self.fixed_lines[j] = self.fixed_lines[j][4:]

                        # 在最后一行后添加结束标记
                        insert_pos = end_line + 1
                        self.fixed_lines.insert(insert_pos, '```\n')
                        self.fixes_applied.append(f'第 {start_line+1}-{end_line+1} 行: 转换为 fenced code block')

    def fix_blank_lines(self):
        """修复多余空行（超过2个连续空行）"""
        i = 0
        while i < len(self.fixed_lines):
            # 计算连续空行数
            blank_count = 0
            j = i
            while j < len(self.fixed_lines) and not self.fixed_lines[j].strip():
                blank_count += 1
                j += 1

            # 如果超过2个，删除多余的
            if blank_count > 2:
                del self.fixed_lines[i+2:j]
                self.fixes_applied.append(f'第 {i+1} 行: 删除 {blank_count-2} 个多余空行')
                i = i + 2  # 跳过剩余的2个空行
            else:
                i = j if blank_count > 0 else i + 1

    def fix_horizontal_rules(self):
        """为水平线添加前后空行"""
        hr_pattern = re.compile(r'^(\*{3,}|-{3,}|_{3,})\s*$')

        for i, line in enumerate(self.fixed_lines):
            if hr_pattern.match(line):
                # 检查前一行是否有空行
                if i > 0 and self.fixed_lines[i-1].strip():
                    self.fixed_lines.insert(i, '\n')
                    self.fixes_applied.append(f'第 {i+1} 行: 水平线前添加空行')
                    i += 1  # 调整索引

                # 检查后一行是否有空行
                if i < len(self.fixed_lines) - 1 and self.fixed_lines[i+1].strip():
                    self.fixed_lines.insert(i+1, '\n')
                    self.fixes_applied.append(f'第 {i+1} 行: 水平线后添加空行')

    def _is_in_code_block(self, line_index: int) -> bool:
        """检查指定行是否在代码块内"""
        in_code = False
        for i in range(min(line_index, len(self.fixed_lines))):
            line = self.fixed_lines[i]
            if line.strip().startswith('```'):
                in_code = not in_code
        return in_code

    def save(self):
        """保存修复后的文件"""
        # 创建备份
        backup_path = self.file_path.with_suffix(self.file_path.suffix + '.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.writelines(self.original_lines)

        # 保存修复后的文件
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.writelines(self.fixed_lines)


def fix_file(file_path: str, dry_run: bool = True) -> dict:
    """修复单个文件"""
    fixer = MarkdownFixer(file_path)
    fixed_lines, fixes = fixer.fix()

    if not dry_run and fixes:
        fixer.save()

    return {
        'file': file_path,
        'fixes': fixes,
        'success': True
    }


def fix_all_files(directory: str, dry_run: bool = True, pattern: str = '') -> List[dict]:
    """修复目录下所有 Markdown 文件"""
    dir_path = Path(directory)
    results = []

    # 查找所有 .md 文件
    if pattern:
        md_files = list(dir_path.rglob(pattern))
    else:
        md_files = list(dir_path.rglob('*.md'))

    print(f'🔧 开始修复 {"(模拟运行)" if dry_run else "(实际修复)"}...\n')

    for i, file_path in enumerate(md_files, 1):
        result = fix_file(str(file_path), dry_run)
        results.append(result)

        if result['fixes']:
            rel_path = str(file_path).replace('/Users/wardlu/Documents/Obsidian Vault/', '')
            print(f'[{i}/{len(md_files)}] ✅ {rel_path}')
            for fix in result['fixes'][:3]:  # 只显示前3个修复
                print(f'         {fix}')
            if len(result['fixes']) > 3:
                print(f'         ... 还有 {len(result["fixes"])-3} 个修复')
            print()

    return results


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='Markdown 语法自动修复工具')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际修改文件')
    parser.add_argument('--pattern', default='', help='文件名模式 (如: *产品*.md)')
    args = parser.parse_args()

    target_dir = '/Users/wardlu/Documents/Obsidian Vault/02_Areas'

    results = fix_all_files(target_dir, dry_run=args.dry_run, pattern=args.pattern)

    # 统计
    total_fixes = sum(len(r['fixes']) for r in results)
    files_with_fixes = sum(1 for r in results if r['fixes'])

    print('=' * 80)
    print(f'📊 修复完成！')
    print(f'   - 处理文件: {len(results)} 个')
    print(f'   - 修复文件: {files_with_fixes} 个')
    print(f'   - 应用修复: {total_fixes} 个')
    print('=' * 80)

    if args.dry_run:
        print('\n💡 这是模拟运行，没有实际修改文件')
        print('💡 如需实际修复，请运行: python3 fix_markdown_syntax.py')


if __name__ == '__main__':
    main()
